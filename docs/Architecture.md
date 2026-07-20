# ConfigVista AI - System Architecture

## Intelligent Network Change Risk Prediction & Decision Support Framework

**Version:** 2.0 (Artifact-1)

**Author:** Shivam Saxena

---

# 1. Introduction

ConfigVista AI is an intelligent decision support framework designed to assist network engineers in assessing the operational risk of Cisco IOS configuration changes before deployment.

The system compares baseline and candidate configurations, identifies configuration differences, classifies changes into networking domains, evaluates operational risk using a rule-based engine, and generates detailed engineering reports.

The architecture has been intentionally designed to support future integration of Machine Learning, Explainable AI (XAI), Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs) without requiring major architectural changes.

---

# 2. System Overview

The application follows a modular layered architecture.

Each layer performs a single responsibility, making the application easier to maintain, extend, and test.

```
                 Streamlit Dashboard
                         │
                         ▼
               Comparison Engine
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     ▼                   ▼                   ▼
 Configuration     Change Classification   Risk Evaluation
     Parser
     │
     ▼
Diff Engine
     │
     ▼
Report Generator
     │
     ▼
SQLite Database
```

---

# 3. High-Level Workflow

```
Baseline Configuration

          +

Candidate Configuration

          │

          ▼

Configuration Normalization

          ▼

Context-aware Parsing

          ▼

Hierarchical Diff Engine

          ▼

Change Classification

          ▼

Risk Evaluation

          ▼

Recommendation Generation

          ▼

Report Generation

          ▼

Dashboard Visualization
```

---

# 4. Layered Architecture

---

## Presentation Layer

### Technology

- Streamlit

### Responsibilities

- Upload baseline configuration
- Upload candidate configuration
- Display comparison results
- Display risk dashboard
- Display category summaries
- Export reports

---

## Comparison Layer

### Components

- Configuration Parser
- Context Mapper
- Diff Engine

### Responsibilities

- Normalize configurations
- Build hierarchical configuration structure
- Detect Added, Removed and Modified changes
- Preserve parent-child relationships

---

## Intelligence Layer

### Components

- Change Classifier
- Risk Evaluator
- Recommendation Engine

### Responsibilities

- Categorize configuration changes
- Calculate risk level
- Generate confidence score
- Produce engineering recommendations

---

## Reporting Layer

### Components

- Report Generator

### Responsibilities

Generate reports in:

- HTML
- Markdown
- JSON
- Plain Text

---

## Persistence Layer

### Technology

SQLite

### Responsibilities

- Store assessment history
- Maintain configuration metadata
- Persist future ML datasets

---

# 5. Component Architecture

```
               Streamlit Dashboard
                        │
                        ▼
            Comparison Engine
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   Config Parser   Diff Engine   Report Generator
        │               │
        ▼               ▼
 Parent Mapper   Change Classifier
                        │
                        ▼
                Risk Evaluator
                        │
                        ▼
              Recommendation Engine
                        │
                        ▼
                 SQLite Database
```

---

# 6. Configuration Comparison Pipeline

The comparison engine follows six sequential processing stages.

---

## Stage 1 — Configuration Normalization

Purpose

- Remove blank lines
- Remove comments
- Normalize whitespace
- Ignore unsupported syntax
- Standardize configuration format

Output

Normalized configuration.

---

## Stage 2 — Context-aware Parsing

Purpose

- Detect parent commands
- Build configuration hierarchy
- Identify configuration blocks
- Preserve parent-child relationships

Examples

```
interface GigabitEthernet0/1
 ip address ...
```

Parent Section

```
interface GigabitEthernet0/1
```

Parent Type

```
interface
```

---

## Stage 3 — Hierarchical Diff Engine

Purpose

Compare:

- Baseline configuration
- Candidate configuration

Detect:

- Added changes
- Removed changes
- Modified changes

Unlike traditional text comparison, the engine preserves networking context.

---

## Stage 4 — Change Classification

Each change is categorized into an engineering domain.

Supported categories:

- Interface
- Routing
- Switching
- Security
- Services
- Management
- System

Examples

```
router ospf
```

↓

Routing

```
access-list
```

↓

Security

```
logging host
```

↓

Management

---

## Stage 5 — Risk Evaluation

The current implementation uses a deterministic rule-based engine.

Each configuration change receives:

- Risk Label
- Risk Score
- Confidence Score
- Recommendation

Example

| Category | Risk |
|-----------|------|
| Interface | Low |
| Switching | Medium |
| Routing | High |
| Security | High |

---

## Stage 6 — Report Generation

Reports include:

- Executive Summary
- Overall Risk
- Statistics
- Category Summary
- Detailed Changes
- Engineering Recommendations

Supported formats

- HTML
- Markdown
- JSON
- Plain Text

---

# 7. Core Modules

## comparison/

Contains the complete comparison framework.

Modules

- comparison_engine.py
- diff_engine.py
- change_classifier.py
- risk_evaluator.py
- report_generator.py
- utils.py
- models.py

---

## parser/

Cisco IOS configuration parsing utilities.

Responsibilities

- Context mapping
- Parent detection
- Configuration normalization

---

## database/

Responsibilities

- Database schema
- Initialization
- Seed data
- Persistence

---

## tests/

Contains:

- Unit Tests
- Integration Tests

---

## docs/

Project documentation.

---

## ml/

Reserved for Machine Learning implementation.

Current status

Planning phase.

---

# 8. Database Architecture

Current database technology:

SQLite

Primary tables include:

- Roles
- Users
- Devices
- Snapshots
- Changes

Future versions may include:

- FeatureStore
- ModelMetrics
- Predictions
- Feedback
- AuditLogs
- TraceLogs

The database schema has been designed to support migration to PostgreSQL with minimal changes.

---

# 9. Design Principles

ConfigVista AI follows the following software engineering principles.

### Layered Architecture

Separates presentation, business logic and persistence.

---

### Separation of Concerns

Each module has a single responsibility.

---

### Modular Design

Components are independently extensible.

---

### Explainability

Every prediction includes engineering reasoning.

---

### Testability

Independent modules enable comprehensive unit testing.

---

### Scalability

Future ML components can be integrated without redesigning the application.

---

# 10. Current Capabilities

Artifact-1 currently supports:

- Context-aware configuration comparison
- Hierarchical parsing
- Intelligent diff engine
- Change classification
- Rule-based risk evaluation
- Engineering recommendations
- Multi-format report generation
- Streamlit dashboard
- SQLite persistence
- Unit testing
- Integration testing

---

# 11. Future Architecture

The next dissertation phase will introduce a Machine Learning layer.

```
                Comparison Engine
                        │
                        ▼
               Feature Engineering
                        │
                        ▼
             Machine Learning Models
            ┌────────────┴────────────┐
            ▼                         ▼
     Random Forest              XGBoost
            │                         │
            └────────────┬────────────┘
                         ▼
                 SHAP Explainability
                         ▼
              Hybrid Risk Prediction
                         ▼
               Recommendation Engine
```

Future enhancements include:

- Feature Engineering
- Dataset Generation
- Random Forest
- XGBoost
- SHAP Explainability
- Hybrid Rule + ML Risk Prediction
- Retrieval-Augmented Generation (RAG)
- Large Language Models
- LangSmith Observability
- Human-in-the-Loop Governance
- Continuous Learning

---

# 12. Conclusion

The current implementation provides a complete end-to-end configuration comparison framework capable of analyzing Cisco IOS configuration changes, evaluating operational risk, and generating engineering recommendations.

The modular architecture forms the baseline software artifact for this dissertation and provides a scalable foundation for the Machine Learning capabilities planned in the next phase of the research.