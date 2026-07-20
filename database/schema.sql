-- database/schema.sql

CREATE TABLE IF NOT EXISTS Roles (

    role_id INTEGER PRIMARY KEY AUTOINCREMENT,

    role_name TEXT NOT NULL UNIQUE,

    description TEXT

);

CREATE TABLE IF NOT EXISTS Users (

    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    full_name TEXT,

    email TEXT,

    role_id INTEGER NOT NULL,

    status TEXT DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(role_id) REFERENCES Roles(role_id)

);

CREATE TABLE IF NOT EXISTS Devices (

    device_id INTEGER PRIMARY KEY AUTOINCREMENT,

    hostname TEXT NOT NULL UNIQUE,

    vendor TEXT,

    model TEXT,

    device_type TEXT,

    management_ip TEXT,

    site TEXT,

    environment TEXT,

    criticality TEXT,

    status TEXT DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS Snapshots (

    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,

    device_id INTEGER,

    snapshot_type TEXT,

    collection_method TEXT,

    snapshot_file TEXT,

    collected_by INTEGER,

    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(device_id) REFERENCES Devices(device_id),

    FOREIGN KEY(collected_by) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS Changes (

    change_id INTEGER PRIMARY KEY AUTOINCREMENT,

    change_reference TEXT UNIQUE,

    device_id INTEGER,

    submitted_by INTEGER,

    change_type TEXT,

    description TEXT,

    risk_label TEXT,

    risk_score REAL,

    confidence_score REAL,

    approval_status TEXT,

    change_status TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(device_id) REFERENCES Devices(device_id),

    FOREIGN KEY(submitted_by) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS Incidents (

    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,

    change_id INTEGER,

    severity TEXT,

    description TEXT,

    rollback_required INTEGER,

    mttr_minutes REAL,

    resolution_status TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(change_id) REFERENCES Changes(change_id)

);

CREATE TABLE IF NOT EXISTS FeatureStore (

    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,

    change_id INTEGER,

    feature_name TEXT,

    feature_value TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(change_id) REFERENCES Changes(change_id)

);

CREATE TABLE IF NOT EXISTS Recommendations (

    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,

    change_id INTEGER,

    recommendation_text TEXT,

    explanation TEXT,

    llm_summary TEXT,

    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(change_id) REFERENCES Changes(change_id)

);

CREATE TABLE IF NOT EXISTS AuditLogs (

    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    action TEXT,

    object_type TEXT,

    object_id INTEGER,

    action_status TEXT,

    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS ScenarioRuns (

    scenario_run_id INTEGER PRIMARY KEY AUTOINCREMENT,

    scenario_name TEXT,

    initiated_by INTEGER,

    change_id INTEGER,

    model_used TEXT,

    overall_status TEXT,

    overall_confidence REAL,

    started_at DATETIME,

    completed_at DATETIME,

    FOREIGN KEY(initiated_by) REFERENCES Users(user_id),

    FOREIGN KEY(change_id) REFERENCES Changes(change_id)

);

CREATE TABLE IF NOT EXISTS TraceLogs (

    trace_id INTEGER PRIMARY KEY AUTOINCREMENT,

    scenario_run_id INTEGER,

    component_name TEXT,

    tool_name TEXT,

    execution_status TEXT,

    latency_ms REAL,

    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(scenario_run_id)
        REFERENCES ScenarioRuns(scenario_run_id)

);

CREATE TABLE IF NOT EXISTS Feedback (

    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,

    change_id INTEGER,

    user_id INTEGER,

    rating INTEGER,

    recommendation_correct INTEGER,

    comments TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(change_id) REFERENCES Changes(change_id),

    FOREIGN KEY(user_id) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS ModelMetrics (

    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,

    model_name TEXT,

    version TEXT,

    accuracy REAL,

    precision_score REAL,

    recall_score REAL,

    f1_score REAL,

    training_time REAL,

    inference_time REAL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE IF NOT EXISTS DatabaseVersion (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT,
    applied_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_change_reference
ON Changes(change_reference);

CREATE INDEX IF NOT EXISTS idx_device_hostname
ON Devices(hostname);

CREATE INDEX IF NOT EXISTS idx_incident_change
ON Incidents(change_id);

CREATE INDEX IF NOT EXISTS idx_trace_run
ON TraceLogs(scenario_run_id);

CREATE INDEX IF NOT EXISTS idx_feature_change
ON FeatureStore(change_id)