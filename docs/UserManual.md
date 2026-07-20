# ConfigVista AI - User Manual

## Intelligent Network Change Risk Prediction & Decision Support Framework

**Version:** 2.0 (Artifact-1)

**Author:** Shivam Saxena

---

# 1. Introduction

ConfigVista AI is an intelligent network change assessment framework developed as part of an MSc dissertation.

The application helps network engineers evaluate Cisco IOS configuration changes before deployment by comparing baseline and candidate configurations, identifying configuration differences, classifying network changes, assessing operational risk, and generating structured engineering recommendations.

The current implementation (Artifact-1) provides a complete rule-based configuration comparison framework that serves as the baseline for future Machine Learning–based risk prediction.

---

# 2. System Requirements

## Operating System

- Windows 10 / Windows 11

## Software

- Python 3.13+
- Git
- Streamlit

## Python Libraries

- Streamlit
- SQLAlchemy
- SQLite
- Paramiko (future use)
- pandas

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

# 3. Starting the Application

## Step 1

Activate the virtual environment.

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Step 2

Launch the Streamlit application.

```bash
streamlit run streamlit_app.py
```

---

## Step 3

The application opens automatically in your default web browser.

---

# 4. Dashboard Overview

The Streamlit dashboard consists of the following sections.

## Configuration Upload

Upload:

- Baseline Configuration
- Candidate Configuration

Supported file formats:

- .txt
- .cfg
- .conf

---

## Executive Summary

Displays:

- Overall Risk
- Average Risk Score
- Confidence Score
- Total Changes
- Added Changes
- Removed Changes
- Modified Changes

---

## Category Summary

Displays configuration changes grouped into:

- Interface
- Routing
- Switching
- Security
- Services
- Management
- System

---

## Detailed Change Analysis

Each detected configuration change includes:

- Change Type
- Parent Section
- Parent Type
- Category
- Risk Level
- Confidence Score
- Recommendation

---

## Report Download

Reports can be exported as:

- HTML
- Markdown
- JSON
- Plain Text

---

# 5. Running a Configuration Comparison

## Step 1

Launch the application.

```bash
streamlit run streamlit_app.py
```

---

## Step 2

Upload the Baseline Cisco IOS configuration.

---

## Step 3

Upload the Candidate Cisco IOS configuration.

---

## Step 4

Click **Compare Configurations**.

---

## Step 5

The application automatically performs:

- Configuration Normalization
- Context-aware Parsing
- Hierarchical Difference Detection
- Change Classification
- Rule-based Risk Evaluation
- Recommendation Generation
- Report Creation

---

## Step 6

Review the generated dashboard.

Sections include:

- Executive Summary
- Risk Dashboard
- Category Summary
- Detailed Changes
- Recommendations

---

# 6. Understanding the Results

## Overall Risk

Represents the highest operational risk detected during comparison.

Possible values:

- Low
- Medium
- High

---

## Risk Score

A numerical score between 0 and 100.

| Score | Risk Level |
|--------|------------|
| 0 – 30 | Low |
| 31 – 60 | Medium |
| 61 – 100 | High |

---

## Confidence Score

Represents the confidence of the rule-based evaluation.

Higher confidence indicates stronger confidence in the assigned risk level.

---

## Change Types

Three types of configuration changes are detected.

### Added

Configuration exists only in the candidate configuration.

---

### Removed

Configuration exists only in the baseline configuration.

---

### Modified

Configuration exists in both files but has different values.

---

# 7. Change Categories

The comparison engine automatically classifies configuration changes into engineering domains.

## Interface

Examples

- IP Address
- Shutdown
- MTU
- Description

---

## Routing

Examples

- OSPF
- EIGRP
- BGP
- Static Routes

---

## Switching

Examples

- VLAN
- Trunk
- STP

---

## Security

Examples

- ACL
- AAA
- Zone Firewall

---

## Management

Examples

- SNMP
- Logging
- NTP

---

## Services

Examples

- DHCP
- DNS
- HTTP
- SSH

---

## System

Examples

- Hostname
- Banner
- Service Configuration

---

# 8. Risk Evaluation

The current implementation uses a deterministic rule-based risk engine.

Typical examples:

| Configuration Area | Risk |
|--------------------|------|
| Interface Description | Low |
| Interface Shutdown | Medium |
| VLAN Changes | Medium |
| Static Route | High |
| OSPF | High |
| BGP | High |
| ACL | High |
| AAA | High |

Each change also includes an engineering recommendation describing the reason for the assigned risk.

---

# 9. Generated Reports

ConfigVista AI generates reports in multiple formats.

## HTML Report

Interactive report suitable for sharing.

---

## Markdown Report

Suitable for documentation.

---

## JSON Report

Machine-readable output for integration.

---

## Plain Text Report

Human-readable console report.

---

# 10. Running Tests

Run the Diff Engine tests.

```bash
python -m tests.test_diff_engine
```

Run the Change Classifier tests.

```bash
python -m tests.test_change_classifier
```

Run the Risk Evaluator tests.

```bash
python -m tests.test_risk_evaluator
```

Run the Integration tests.

```bash
python -m tests.test_comparison_engine
```

---

# 11. Troubleshooting

## Streamlit does not start

Verify Streamlit installation.

```bash
streamlit --version
```

---

## Missing Python packages

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Database initialization

Create the database.

```bash
python -m database.initialize_db
```

---

## Empty database

Seed sample data.

```bash
python -m database.seed_data
```

---

## Import errors

Ensure the virtual environment is activated before running the application.

---

# 12. Current Implementation

Artifact-1 currently includes:

- Context-aware configuration parser
- Hierarchical diff engine
- Change classification engine
- Rule-based risk evaluation
- Recommendation generation
- Report generation
- Streamlit dashboard
- SQLite persistence
- Unit tests
- Integration tests

---

# 13. Current Limitations

The current implementation does not yet include:

- Machine Learning prediction
- Random Forest
- XGBoost
- SHAP explainability
- Live SSH device collection
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- LangSmith observability
- Human-in-the-Loop approval workflow

These capabilities will be introduced in later dissertation phases.

---

# 14. Future Enhancements

Planned enhancements include:

- Machine Learning risk prediction
- Random Forest classifier
- XGBoost classifier
- Explainable AI using SHAP
- Hybrid Rule + ML prediction
- Live network device integration
- RAG-based recommendation engine
- LangSmith tracing
- Continuous learning pipeline
- Enterprise database support

---

# 15. Support

## Author

**Shivam Saxena**

MSc Dissertation

**Project:** ConfigVista AI

---

## Version History

| Version | Description |
|----------|-------------|
| 1.0 | Initial MVP |
| 2.0 | Configuration Comparison Framework (Artifact-1) |