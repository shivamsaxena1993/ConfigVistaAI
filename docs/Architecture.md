# ConfigVista AI - System Architecture

## Intelligent Network Change Risk Prediction & Decision Support Framework

**Version:** MVP 1.0

---

# 1. Introduction

ConfigVista AI follows a layered software architecture that separates presentation, business logic, persistence, and data management into independent modules.

This design improves maintainability, scalability, and future extensibility while supporting the planned integration of Machine Learning and Large Language Models.

---

# 2. High-Level Architecture

```
                 Streamlit Dashboard
                        │
                        ▼
                 Assessment Service
                        │
                        ▼
     ┌─────────────────────────────────┐
     │                                 │
Parser → Feature Extraction → Risk Engine
     │                                 │
     └──────── Recommendation Engine ──┘
                        │
                        ▼
               Persistence Service
                        │
                        ▼
              SQLite Knowledge Base
```

---

# 3. Layered Architecture

## Presentation Layer

Technology

- Streamlit

Responsibilities

- Configuration upload
- Dashboard rendering
- Risk visualization
- Recommendation display
- Knowledge Base

---

## Service Layer

Components

- AssessmentService
- PersistenceService
- HistoryService

Responsibilities

- Orchestrate workflow
- Manage application logic
- Persist assessments
- Retrieve historical data

---

## Parser Layer

Components

- ConfigParser
- FeatureExtractor

Responsibilities

- Parse Cisco configurations
- Extract engineering features
- Normalize configuration data

---

## Intelligence Layer

Components

- RiskEngine
- RecommendationEngine

Responsibilities

- Predict operational risk
- Calculate confidence score
- Generate explainable recommendations

---

## Persistence Layer

Components

- SQLAlchemy ORM
- Repository Pattern

Responsibilities

- CRUD operations
- Database abstraction
- Transaction management

---

## Database Layer

Technology

SQLite

Tables

- Roles
- Users
- Devices
- Snapshots
- Changes
- Incidents
- FeatureStore
- Recommendations
- AuditLogs
- TraceLogs
- Feedback
- ModelMetrics
- ScenarioRuns
- DatabaseVersion

---

# 4. Assessment Workflow

```
Cisco Configuration

        │

        ▼

Configuration Parser

        │

        ▼

Feature Extraction

        │

        ▼

Risk Prediction

        │

        ▼

Recommendation Engine

        │

        ▼

Persistence Layer

        │

        ▼

Knowledge Base

        │

        ▼

Dashboard
```

---

# 5. Repository Pattern

The application follows the Repository Pattern to isolate business logic from persistence.

Advantages include:

- Separation of concerns
- Reusable CRUD operations
- Easier testing
- Cleaner code
- Database independence

Current repositories include:

- DeviceRepository
- ChangeRepository
- IncidentRepository
- SnapshotRepository
- RecommendationRepository
- FeedbackRepository
- MetricsRepository
- AuditRepository

---

# 6. Database Design

SQLite is used during the MVP phase to provide a lightweight embedded database.

The schema is normalized and designed to support future migration to enterprise databases such as PostgreSQL.

Historical assessments form the foundation of the AI Knowledge Base.

---

# 7. Explainable AI

Unlike a traditional black-box prediction model, ConfigVista AI provides transparent reasoning behind every risk score.

Each prediction includes:

- Risk Score
- Risk Label
- Confidence Score
- Contributing Factors
- Engineering Explanation

This enables engineers to understand why a recommendation was generated.

---

# 8. Design Principles

The project follows:

- Layered Architecture
- Repository Pattern
- Service Layer Pattern
- Modular UI Components
- Explainable AI
- Separation of Concerns
- Clean Code Principles
- Scalability

---

# 9. Future Architecture

Future dissertation work will extend the architecture by introducing:

- Random Forest
- XGBoost
- SHAP Explainability
- Retrieval-Augmented Generation (RAG)
- Large Language Models
- LangSmith Observability
- Human-in-the-Loop Governance
- Live SSH Device Collection
- Continuous Learning Pipeline

The existing architecture has been designed so these capabilities can be integrated without major structural changes.

---

# 10. Conclusion

The current MVP demonstrates an end-to-end intelligent assessment workflow, from configuration parsing through risk prediction and recommendation generation to persistent storage and visualization.

The layered architecture provides a robust foundation for the advanced AI and Machine Learning capabilities planned for the final dissertation.