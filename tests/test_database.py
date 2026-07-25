"""
ConfigVista AI - Database Integration Tests

Validates the SQLAlchemy persistence layer using an isolated
temporary SQLite database.

The production/local ConfigVista database is never modified.
"""

import pytest

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from database.database import Base
from database.models import (
    Role,
    User,
    Device,
    Snapshot,
    Change,
    Recommendation,
    AuditLog,
)
from database.repositories.device_repository import DeviceRepository
from database.repositories.change_repository import ChangeRepository
from database.repositories.snapshot_repository import SnapshotRepository
from database.repositories.recommendation_repository import (
    RecommendationRepository,
)
from database.repositories.audit_repository import AuditRepository


# ==========================================================
# DATABASE FIXTURE
# ==========================================================

@pytest.fixture()
def session(tmp_path):

    db_path = tmp_path / "configvista_test.db"

    engine = create_engine(
        f"sqlite:///{db_path}",
        future=True,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(
        dbapi_connection,
        connection_record,
    ):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True,
    )

    Base.metadata.create_all(engine)

    db_session = TestingSession()

    try:
        yield db_session
    finally:
        db_session.rollback()
        db_session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


# ==========================================================
# TEST DATA
# ==========================================================

def create_identity(session):

    role = Role(
        role_name="Network Engineer",
        description="Network operations engineer",
    )

    session.add(role)
    session.flush()

    user = User(
        username="test_engineer",
        full_name="Test Engineer",
        email="engineer@example.test",
        role_id=role.role_id,
        status="Active",
    )

    session.add(user)
    session.flush()

    return role, user


def create_device(session):

    device = Device(
        hostname="Branch-RTR01",
        vendor="Cisco",
        model="ISR4331",
        device_type="Router",
        management_ip="10.20.1.1",
        site="Branch-01",
        environment="Production",
        criticality="High",
        status="Active",
    )

    session.add(device)
    session.flush()

    return device


def create_change(session, device, user):

    change = Change(
        change_reference="CHG-TEST-001",
        device_id=device.device_id,
        submitted_by=user.user_id,
        change_type="Routing",
        description="Modify branch routing configuration",
        risk_label="High",
        risk_score=82.5,
        confidence_score=91.0,
        approval_status="Pending",
        change_status="Submitted",
    )

    session.add(change)
    session.flush()

    return change


# ==========================================================
# SCHEMA / DATABASE TESTS
# ==========================================================

def test_database_schema_created(session):

    bind = session.get_bind()

    table_names = set(
        Base.metadata.tables.keys()
    )

    required = {
        "Roles",
        "Users",
        "Devices",
        "Snapshots",
        "Changes",
        "Incidents",
        "FeatureStore",
        "Recommendations",
        "AuditLogs",
        "ScenarioRuns",
        "TraceLogs",
        "Feedback",
        "ModelMetrics",
        "DatabaseVersion",
    }

    assert required.issubset(table_names)


def test_sqlite_foreign_keys_enabled(session):

    value = session.connection().exec_driver_sql(
        "PRAGMA foreign_keys"
    ).scalar()

    assert value == 1


# ==========================================================
# DEVICE REPOSITORY
# ==========================================================

def test_device_repository_crud(session):

    repository = DeviceRepository(session)

    device = Device(
        hostname="Core-R1",
        vendor="Cisco",
        model="Catalyst 9500",
        device_type="Switch",
        management_ip="10.10.1.1",
        site="DC1",
        environment="Production",
        criticality="High",
        status="Active",
    )

    repository.add(device)

    assert device.device_id is not None
    assert repository.count() == 1
    assert repository.exists(device.device_id)

    stored = repository.get_by_hostname("Core-R1")

    assert stored is not None
    assert stored.vendor == "Cisco"

    stored.site = "DC-PRIMARY"

    repository.update(stored)

    updated = repository.get_by_id(device.device_id)

    assert updated.site == "DC-PRIMARY"

    repository.delete(updated)

    assert repository.count() == 0


def test_device_repository_domain_queries(session):

    repository = DeviceRepository(session)

    repository.add(
        Device(
            hostname="Core-R1",
            vendor="Cisco",
            model="C9500",
            device_type="Switch",
            site="DC1",
            environment="Production",
            criticality="High",
            status="Active",
        )
    )

    repository.add(
        Device(
            hostname="Lab-R1",
            vendor="Cisco",
            model="CSR1000v",
            device_type="Router",
            site="LAB",
            environment="Development",
            criticality="Low",
            status="Inactive",
        )
    )

    assert len(repository.get_by_vendor("Cisco")) == 2
    assert len(repository.get_by_site("DC1")) == 1
    assert len(repository.get_by_environment("Production")) == 1
    assert len(repository.get_active_devices()) == 1
    assert len(repository.get_critical_devices()) == 1
    assert repository.hostname_exists("Core-R1")
    assert len(repository.search_devices("Core")) == 1


# ==========================================================
# CHANGE REPOSITORY
# ==========================================================

def test_change_repository(session):

    _, user = create_identity(session)
    device = create_device(session)

    repository = ChangeRepository(session)

    change = Change(
        change_reference="CHG-TEST-001",
        device_id=device.device_id,
        submitted_by=user.user_id,
        change_type="Routing",
        description="BGP routing modification",
        risk_label="High",
        risk_score=88.0,
        confidence_score=94.0,
        approval_status="Pending",
        change_status="Submitted",
    )

    repository.add(change)

    assert change.change_id is not None

    assert (
        repository.get_by_reference(
            "CHG-TEST-001"
        ).change_id
        == change.change_id
    )

    assert len(
        repository.get_high_risk_changes()
    ) == 1

    assert len(
        repository.get_pending_approvals()
    ) == 1

    assert len(
        repository.get_by_status("Submitted")
    ) == 1


# ==========================================================
# SNAPSHOT REPOSITORY
# ==========================================================

def test_snapshot_repository(session):

    _, user = create_identity(session)
    device = create_device(session)

    repository = SnapshotRepository(session)

    snapshot = Snapshot(
        device_id=device.device_id,
        snapshot_type="Pre-Change",
        collection_method="Upload",
        snapshot_file="branch-rtr01-pre.cfg",
        collected_by=user.user_id,
    )

    repository.add(snapshot)

    assert snapshot.snapshot_id is not None

    latest = repository.get_latest_snapshot(
        device.device_id
    )

    assert latest is not None

    assert latest.snapshot_type == "Pre-Change"

    history = repository.get_snapshot_history(
        device.device_id
    )

    assert len(history) == 1

    assert len(
        repository.get_by_snapshot_type(
            "Pre-Change"
        )
    ) == 1


# ==========================================================
# RECOMMENDATION REPOSITORY
# ==========================================================

def test_recommendation_repository(session):

    _, user = create_identity(session)
    device = create_device(session)
    change = create_change(
        session,
        device,
        user,
    )

    repository = RecommendationRepository(
        session
    )

    recommendation = Recommendation(
        change_id=change.change_id,
        recommendation_text=(
            "Validate routing adjacency "
            "before deployment."
        ),
        explanation=(
            "Routing changes have elevated "
            "operational impact."
        ),
        llm_summary=None,
    )

    repository.add(recommendation)

    results = repository.get_by_change(
        change.change_id
    )

    assert len(results) == 1

    assert (
        results[0].recommendation_id
        == recommendation.recommendation_id
    )

    latest = repository.get_latest()

    assert latest is not None


# ==========================================================
# AUDIT REPOSITORY
# ==========================================================

def test_audit_repository(session):

    _, user = create_identity(session)

    repository = AuditRepository(session)

    log = AuditLog(
        user_id=user.user_id,
        action="CREATE_CHANGE",
        object_type="Change",
        object_id=1,
        action_status="Success",
    )

    repository.add(log)

    activity = repository.get_user_activity(
        user.user_id
    )

    assert len(activity) == 1

    assert activity[0].action == "CREATE_CHANGE"

    by_action = repository.get_by_action(
        "CREATE_CHANGE"
    )

    assert len(by_action) == 1


# ==========================================================
# CONSTRAINT / TRANSACTION TESTS
# ==========================================================

def test_unique_hostname_constraint(session):

    repository = DeviceRepository(session)

    repository.add(
        Device(hostname="Duplicate-R1")
    )

    with pytest.raises(IntegrityError):

        repository.add(
            Device(hostname="Duplicate-R1")
        )

    session.rollback()


def test_foreign_key_constraint(session):

    invalid_change = Change(
        change_reference="CHG-INVALID",
        device_id=999999,
        submitted_by=999999,
        change_type="Routing",
    )

    session.add(invalid_change)

    with pytest.raises(IntegrityError):
        session.flush()

    session.rollback()