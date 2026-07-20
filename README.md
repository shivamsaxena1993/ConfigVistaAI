# 🛰️ ConfigVista AI

## Intelligent Network Change Risk Prediction & Decision Support Framework

**MSc Dissertation Prototype**

---

# Overview

ConfigVista AI is an AI-assisted decision support framework that helps network engineers assess the operational risk of network configuration changes before deployment.

The framework analyzes Cisco IOS configuration files, extracts networking features, validates the extracted data, predicts operational risk using an explainable rule-based engine, generates actionable recommendations, and stores assessment history in a centralized knowledge base.

The current implementation represents the **Phase 1 MVP** of the dissertation and establishes the foundation for future Machine Learning, Explainable AI, Retrieval-Augmented Generation (RAG), Configuration Comparison, and Human-in-the-Loop governance.

---

# Problem Statement

Enterprise networks undergo thousands of configuration changes throughout their lifecycle.

Current change reviews are largely manual and depend heavily on engineer expertise, leading to:

- Inconsistent risk evaluation
- Human error
- Longer implementation windows
- Limited reuse of historical knowledge
- Increased probability of service outages

ConfigVista AI aims to provide a consistent, explainable, and reusable framework that assists engineers in evaluating network change risk before implementation.

---

# Dissertation Objectives

The project aims to:

- Parse Cisco IOS configuration files
- Automatically extract networking features
- Validate extracted features
- Predict operational risk
- Generate explainable recommendations
- Persist historical assessments
- Build a searchable knowledge repository
- Provide an intuitive dashboard for network engineers
- Establish the foundation for ML-driven risk prediction

---

# Phase 1 MVP Features

## Configuration Parsing

- Cisco IOS Configuration Parser
- Interface Discovery
- VLAN Detection
- Routing Protocol Discovery
- ACL Detection
- Route Map Detection
- Prefix List Detection
- VRF Detection

---

## Feature Engineering

Automatically extracts networking characteristics including:

- Device Information
- Interface Count
- VLAN Count
- ACL Count
- Static Routes
- Routing Protocols
- NAT
- QoS
- VPN
- AAA
- SNMP
- SSH
- Route Maps
- Prefix Lists
- VRFs
- Configuration Complexity Score

---

## Feature Validation

All extracted features pass through a validation layer that:

- Applies default values
- Normalizes data types
- Prevents invalid values
- Recalculates derived metrics
- Produces a canonical feature representation

---

## Risk Prediction Engine

Current MVP uses an explainable rule-based engine that generates:

- Risk Score
- Risk Label
- Confidence Score
- Risk Summary
- Risk Explanations

---

## Recommendation Engine

Automatically generates:

- Pre-check recommendations
- Implementation guidance
- Validation checks
- Monitoring recommendations
- Rollback recommendations

---

## Persistence Layer

Assessment results are stored in SQLite including:

- Configuration Features
- Risk Assessment
- Recommendations
- Confidence Score
- Assessment Timestamp
- Historical Assessments

---

## Streamlit Dashboard

Interactive dashboard providing:

- Configuration Upload
- Assessment Summary
- Configuration Overview
- Risk Visualization
- Explainable AI
- Recommendations
- Knowledge Base

---

# Current System Architecture

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
               Feature Validation
                          │
                          ▼
               Risk Prediction Engine
                          │
                          ▼
             Recommendation Engine
                          │
                          ▼
                Persistence Service
                          │
                          ▼
                  SQLite Database
                          │
                          ▼
                 Streamlit Dashboard
```

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.13 |
| UI | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| ML Prototype | Rule-Based Risk Engine |
| Future ML | Random Forest |
| Future ML | XGBoost |
| Explainability | Rule Explanations |
| Version Control | Git |

---

# Project Structure

```
ConfigVistaAI/

├── app/
├── configs/
├── data/
├── database/
├── docs/
├── governance/
├── logs/
├── ml/
├── mock_devices/
├── models/
├── observability/
├── parser/
├── services/
├── tests/
├── tools/
├── ui/
├── utils/
│
├── streamlit_app.py
├── main.py
├── requirements.txt
├── requirements-lock.txt
├── README.md
└── .gitignore
```

---

# Assessment Pipeline

The assessment workflow follows a modular service-oriented architecture.

```
Configuration File
        │
        ▼
Configuration Parser
        │
        ▼
Feature Extraction
        │
        ▼
Feature Validation
        │
        ▼
Risk Engine
        │
        ▼
Recommendation Engine
        │
        ▼
Persistence Service
        │
        ▼
SQLite Knowledge Base
```

---

# Database

Current database entities include:

- Roles
- Users
- Devices
- Snapshots
- Changes
- Incidents
- FeatureStore
- Recommendations
- AuditLogs
- ScenarioRuns
- TraceLogs
- Feedback
- ModelMetrics
- DatabaseVersion

The project follows the **Repository Pattern** for clean separation between business logic and persistence.

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<username>/ConfigVistaAI.git

cd ConfigVistaAI
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Database Initialization

Initialize the SQLite database.

```bash
python -m database.initialize_db
```

(Optional) Seed sample data.

```bash
python -m database.seed_data
```

---

# Running the Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard provides:

- Configuration Upload
- Risk Assessment
- Explainable AI
- Recommendations
- Knowledge Base
- Assessment History

---

# Running End-to-End Tests

Run the assessment pipeline against the sample configurations.

```bash
python -m tests.test_pipeline
```

Expected output:

```
=========================================================
ConfigVista AI - End-to-End Pipeline Test
=========================================================

Testing : Cat9k-Core-Switch01.txt
PASS

Testing : Cat9k-L2-Stack01.txt
PASS

Testing : CE-Router-01.txt
PASS

Testing : Internet-GW01.txt
PASS

=========================================================
Passed : 4/4
=========================================================
```

---

# Sample Assessment

Example output:

| Metric | Value |
|---------|-------|
| Risk Score | 60 |
| Risk Label | Medium |
| Confidence | 84% |
| Priority | P2 |
| Recommendations | 11 |

---

# Design Principles

The project follows:

- Layered Architecture
- Service Layer Pattern
- Repository Pattern
- Separation of Concerns
- Explainable AI
- Modular Components
- Clean Code Principles

---

# Current Project Status

## ✅ Phase 1 – Assessment Pipeline (Completed)

- Configuration Parser
- Feature Extraction
- Feature Validation
- Rule-Based Risk Engine
- Recommendation Engine
- SQLite Persistence
- Streamlit Dashboard
- End-to-End Testing
- Knowledge Base

---

## 🚧 Phase 2 – Configuration Comparison

Planned capabilities:

- Baseline Configuration
- Candidate Configuration
- Configuration Difference Engine
- Change Feature Generation
- Change-Aware Risk Assessment

---

## 🚧 Phase 3 – Machine Learning

- Random Forest
- XGBoost
- Model Evaluation
- Feature Importance
- SHAP Explainability

---

## 🚧 Phase 4 – AI Decision Support

- Retrieval-Augmented Generation (RAG)
- LLM-Assisted Recommendations
- Historical Similarity Search
- Intelligent Risk Explanation

---

## 🚧 Phase 5 – Enterprise Integration

- Live SSH Collection
- Device Telemetry
- Human-in-the-Loop Governance
- LangSmith Observability
- Continuous Learning

---

# Future Roadmap

- Configuration Comparison Engine
- Historical Change Analysis
- Machine Learning Risk Prediction
- Explainable AI using SHAP
- Retrieval-Augmented Generation
- Human Approval Workflow
- Live Device Integration
- Continuous Model Improvement

---

# Author

**Shivam Saxena**

MSc Dissertation

**ConfigVista AI**

Intelligent Network Change Risk Prediction & Decision Support Framework

2026

---

# License

This project has been developed for academic research and dissertation purposes.

All rights reserved.