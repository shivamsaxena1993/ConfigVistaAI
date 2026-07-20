"""
====================================================================
File: models.py

Project : ConfigVista AI

Purpose
-------
SQLAlchemy ORM Models

Part-1
------
Role
User
Device
Snapshot
====================================================================
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


# ============================================================
# Roles
# ============================================================
class Role(Base):
    __tablename__ = "Roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True, nullable=False)
    description = Column(Text)

    # Relationships
    users = relationship(
        "User",
        back_populates="role",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Role(role_name='{self.role_name}')>"


# ============================================================
# Users
# ============================================================
class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    email = Column(String)
    role_id = Column(
        Integer,
        ForeignKey("Roles.role_id"),
        nullable=False
    )
    status = Column(String, default="Active")
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    # Relationships
    role = relationship(
        "Role",
        back_populates="users"
    )
    snapshots = relationship(
        "Snapshot",
        back_populates="collector"
    )
    changes = relationship(
        "Change",
        back_populates="submitted_user"
    )
    audit_logs = relationship(
        "AuditLog",
        back_populates="user"
    )
    feedback = relationship(
        "Feedback",
        back_populates="user"
    )
    scenarios = relationship(
        "ScenarioRun",
        back_populates="initiator"
    )

    def __repr__(self):
        return f"<User(username='{self.username}')>"


# ============================================================
# Devices
# ============================================================
class Device(Base):
    __tablename__ = "Devices"

    device_id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String, unique=True, nullable=False)
    vendor = Column(String)
    model = Column(String)
    device_type = Column(String)
    management_ip = Column(String)
    site = Column(String)
    environment = Column(String)
    criticality = Column(String)
    status = Column(String, default="Active")
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    # Relationships
    snapshots = relationship(
        "Snapshot",
        back_populates="device"
    )
    changes = relationship(
        "Change",
        back_populates="device"
    )

    def __repr__(self):
        return f"<Device(hostname='{self.hostname}')>"


# ============================================================
# Snapshots
# ============================================================
class Snapshot(Base):
    __tablename__ = "Snapshots"

    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(
        Integer,
        ForeignKey("Devices.device_id")
    )
    snapshot_type = Column(String)
    collection_method = Column(String)
    snapshot_file = Column(String)
    collected_by = Column(
        Integer,
        ForeignKey("Users.user_id")
    )
    collected_at = Column(
        DateTime,
        server_default=func.now()
    )

    # Relationships
    device = relationship(
        "Device",
        back_populates="snapshots"
    )
    collector = relationship(
        "User",
        back_populates="snapshots"
    )

    def __repr__(self):
        return (
            f"<Snapshot("
            f"device={self.device_id}, "
            f"type='{self.snapshot_type}')>"
        )
    

# ============================================================
# Changes
# ============================================================
class Change(Base):
    __tablename__ = "Changes"

    change_id = Column(Integer, primary_key=True, autoincrement=True)
    change_reference = Column(String, unique=True)
    device_id = Column(
        Integer,
        ForeignKey("Devices.device_id")
    )
    submitted_by = Column(
        Integer,
        ForeignKey("Users.user_id")
    )
    change_type = Column(String)
    description = Column(Text)
    risk_label = Column(String)
    risk_score = Column(Float)
    confidence_score = Column(Float)
    approval_status = Column(String)
    change_status = Column(String)
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------
    device = relationship(
        "Device",
        back_populates="changes"
    )
    submitted_user = relationship(
        "User",
        back_populates="changes"
    )
    incidents = relationship(
        "Incident",
        back_populates="change",
        cascade="all, delete-orphan"
    )
    features = relationship(
        "FeatureStore",
        back_populates="change",
        cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "Recommendation",
        back_populates="change",
        cascade="all, delete-orphan"
    )
    feedback = relationship(
        "Feedback",
        back_populates="change",
        cascade="all, delete-orphan"
    )
    scenarios = relationship(
        "ScenarioRun",
        back_populates="change",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Change("
            f"reference='{self.change_reference}', "
            f"risk='{self.risk_label}')>"
        )


# ============================================================
# Incidents
# ============================================================
class Incident(Base):
    __tablename__ = "Incidents"

    incident_id = Column(Integer, primary_key=True, autoincrement=True)
    change_id = Column(
        Integer,
        ForeignKey("Changes.change_id")
    )
    severity = Column(String)
    description = Column(Text)
    rollback_required = Column(Integer)
    mttr_minutes = Column(Float)
    resolution_status = Column(String)
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    change = relationship(
        "Change",
        back_populates="incidents"
    )

    def __repr__(self):
        return (
            f"<Incident("
            f"severity='{self.severity}')>"
        )


# ============================================================
# Feature Store
# ============================================================
class FeatureStore(Base):
    __tablename__ = "FeatureStore"

    feature_id = Column(Integer, primary_key=True, autoincrement=True)
    change_id = Column(
        Integer,
        ForeignKey("Changes.change_id")
    )
    feature_name = Column(String)
    feature_value = Column(String)
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    change = relationship(
        "Change",
        back_populates="features"
    )

    def __repr__(self):
        return (
            f"<Feature("
            f"{self.feature_name}={self.feature_value})>"
        )


# ============================================================
# Recommendations
# ============================================================
class Recommendation(Base):
    __tablename__ = "Recommendations"

    recommendation_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    change_id = Column(
        Integer,
        ForeignKey("Changes.change_id")
    )
    recommendation_text = Column(Text)
    explanation = Column(Text)
    llm_summary = Column(Text)
    generated_at = Column(
        DateTime,
        server_default=func.now()
    )

    change = relationship(
        "Change",
        back_populates="recommendations"
    )

    def __repr__(self):
        return (
            f"<Recommendation("
            f"id={self.recommendation_id})>"
        )
    
# ============================================================
# Audit Logs
# ============================================================

class AuditLog(Base):

    __tablename__ = "AuditLogs"

    audit_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("Users.user_id")
    )

    action = Column(String)

    object_type = Column(String)

    object_id = Column(Integer)

    action_status = Column(String)

    timestamp = Column(
        DateTime,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="audit_logs"
    )

    def __repr__(self):

        return (
            f"<AuditLog("
            f"user={self.user_id}, "
            f"action='{self.action}')>"
        )


# ============================================================
# Scenario Runs
# ============================================================

class ScenarioRun(Base):

    __tablename__ = "ScenarioRuns"

    scenario_run_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    scenario_name = Column(String)

    initiated_by = Column(
        Integer,
        ForeignKey("Users.user_id")
    )

    change_id = Column(
        Integer,
        ForeignKey("Changes.change_id")
    )

    model_used = Column(String)

    overall_status = Column(String)

    overall_confidence = Column(Float)

    started_at = Column(DateTime)

    completed_at = Column(DateTime)

    initiator = relationship(
        "User",
        back_populates="scenarios"
    )

    change = relationship(
        "Change",
        back_populates="scenarios"
    )

    trace_logs = relationship(
        "TraceLog",
        back_populates="scenario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<ScenarioRun("
            f"id={self.scenario_run_id}, "
            f"status='{self.overall_status}')>"
        )


# ============================================================
# Trace Logs
# ============================================================

class TraceLog(Base):

    __tablename__ = "TraceLogs"

    trace_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    scenario_run_id = Column(
        Integer,
        ForeignKey("ScenarioRuns.scenario_run_id")
    )

    component_name = Column(String)

    tool_name = Column(String)

    execution_status = Column(String)

    latency_ms = Column(Float)

    timestamp = Column(
        DateTime,
        server_default=func.now()
    )

    scenario = relationship(
        "ScenarioRun",
        back_populates="trace_logs"
    )

    def __repr__(self):

        return (
            f"<TraceLog("
            f"component='{self.component_name}')>"
        )


# ============================================================
# Feedback
# ============================================================

class Feedback(Base):

    __tablename__ = "Feedback"

    feedback_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    change_id = Column(
        Integer,
        ForeignKey("Changes.change_id")
    )

    user_id = Column(
        Integer,
        ForeignKey("Users.user_id")
    )

    rating = Column(Integer)

    recommendation_correct = Column(Integer)

    comments = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    change = relationship(
        "Change",
        back_populates="feedback"
    )

    user = relationship(
        "User",
        back_populates="feedback"
    )

    def __repr__(self):

        return (
            f"<Feedback("
            f"rating={self.rating})>"
        )


# ============================================================
# Model Metrics
# ============================================================

class ModelMetric(Base):

    __tablename__ = "ModelMetrics"

    metric_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    model_name = Column(String)

    version = Column(String)

    accuracy = Column(Float)

    precision_score = Column(Float)

    recall_score = Column(Float)

    f1_score = Column(Float)

    training_time = Column(Float)

    inference_time = Column(Float)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    def __repr__(self):

        return (
            f"<ModelMetric("
            f"model='{self.model_name}')>"
        )


# ============================================================
# Database Version
# ============================================================

class DatabaseVersion(Base):

    __tablename__ = "DatabaseVersion"

    version_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    version = Column(String)

    applied_on = Column(
        DateTime,
        server_default=func.now()
    )

    description = Column(Text)

    def __repr__(self):

        return (
            f"<DatabaseVersion("
            f"version='{self.version}')>"
        )
    
