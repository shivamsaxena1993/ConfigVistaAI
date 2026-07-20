# ConfigVista AI

## Intelligent Network Change Risk Prediction & Decision Support Framework

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-Phase%202%20Complete-success)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## Overview

ConfigVista AI is an intelligent network change assessment framework developed as part of an MSc dissertation.

The project assists network engineers in evaluating Cisco IOS configuration changes before deployment by automatically comparing configurations, classifying network changes, estimating operational risk, and generating actionable implementation recommendations.

The current implementation (Artifact-1) provides a complete rule-based configuration comparison framework that serves as the baseline for future Machine Learning–based risk prediction.

---

# Key Features

### Configuration Comparison

- Compare Baseline and Candidate Cisco IOS configurations
- Detect Added, Removed and Modified configuration lines
- Hierarchical configuration parsing
- Context-aware parent section mapping

### Change Classification

Automatically categorizes configuration changes into:

- Interface
- Routing
- Switching
- Security
- Services
- Management
- System

### Risk Evaluation

Rule-based operational risk prediction including:

- Risk Label
- Risk Score
- Confidence Score
- Engineering Recommendation

### Reporting

Generate reports in multiple formats:

- HTML
- Markdown
- JSON
- Plain Text

### Interactive Dashboard

Streamlit dashboard provides:

- Configuration upload
- Executive Summary
- Risk Dashboard
- Category Summary
- Detailed Change Analysis
- Downloadable Reports

---

# Current Architecture

```
           Baseline Configuration
                     │
                     │
                     ▼
          Configuration Normalization
                     │
                     ▼
            Context-aware Parser
                     │
                     ▼
             Hierarchical Diff Engine
                     │
                     ▼
          Change Classification Engine
                     │
                     ▼
             Rule-based Risk Engine
                     │
                     ▼
              Report Generation
                     │
                     ▼
             Streamlit Dashboard
```

---

# Repository Structure

```
ConfigVistaAI/

│
├── comparison/                 # Configuration comparison engine
├── comparison_examples/        # Sample configurations
├── configs/                    # Runtime configurations
├── data/                       # Sample datasets
├── database/                   # SQLite database & schema
├── docs/                       # Documentation
├── logs/                       # Application logs
├── ml/                         # Machine Learning (Phase 3)
├── mock_devices/               # Simulated device outputs
├── models/                     # ML models
├── observability/              # Monitoring & tracing
├── parser/                     # Cisco configuration parser
├── services/                   # Business logic
├── tests/                      # Unit & integration tests
├── tools/                      # Utility scripts
├── ui/                         # UI components
│
├── streamlit_app.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.13 |
| UI | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| Testing | unittest |
| Version Control | Git / GitHub |

---

# Current Workflow

```
Baseline Configuration

        +

Candidate Configuration

        │

        ▼

Normalization

        ▼

Context-aware Parsing

        ▼

Diff Engine

        ▼

Change Classification

        ▼

Risk Evaluation

        ▼

Report Generation

        ▼

Dashboard Visualization
```

---

# Example Output

The comparison engine produces:

- Executive Summary
- Overall Risk
- Average Risk Score
- Confidence Score
- Added Changes
- Removed Changes
- Modified Changes
- Category Summary
- Detailed Change Analysis
- Engineering Recommendations

---

# Installation

Clone the repository

```bash
git clone https://github.com/shivamsaxena1993/ConfigVistaAI.git

cd ConfigVistaAI
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Launch Streamlit

```bash
streamlit run streamlit_app.py
```

The application opens in your browser.

---

# Running Unit Tests

Run Diff Engine tests

```bash
python -m tests.test_diff_engine
```

Run Classifier tests

```bash
python -m tests.test_change_classifier
```

Run Risk Evaluator tests

```bash
python -m tests.test_risk_evaluator
```

Run Integration Tests

```bash
python -m tests.test_comparison_engine
```

---

# Current Project Status

## Phase 1 — MVP

Completed

- Configuration Parser
- Feature Extraction
- Initial Risk Assessment
- SQLite Database
- Streamlit Dashboard

---

## Phase 2 — Artifact-1

Completed

- Context-aware Parser
- Hierarchical Diff Engine
- Change Classification
- Rule-based Risk Evaluation
- Report Generator
- Executive Dashboard
- HTML / Markdown / JSON Reports
- Unit Testing
- Integration Testing
- Repository Cleanup

---

## Phase 3 — Machine Learning (Planned)

Upcoming work includes:

- Dataset Generation
- Feature Engineering
- Random Forest Model
- XGBoost Model
- Model Evaluation
- SHAP Explainability
- ML Risk Prediction
- Hybrid Rule + ML Engine

---

# Dissertation Objective

The research investigates whether Machine Learning can improve the prediction of operational risk associated with Cisco IOS configuration changes compared with deterministic rule-based assessment.

The completed comparison engine provides the baseline against which future ML models will be evaluated.

---

# Documentation

Project documentation is available in the **docs/** directory.

- User Manual
- System Architecture
- Database Design
- Development Notes

---

# Future Enhancements

- Live SSH Device Collection
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- LangSmith Observability
- Human-in-the-Loop Approval Workflow
- Continuous Learning Pipeline
- Enterprise Database Support
- REST API

---

# Author

**Shivam Saxena**

MSc Dissertation

**ConfigVista AI**

---

# Acknowledgements

This project is being developed as part of an MSc dissertation focusing on Intelligent Network Operations, Explainable AI, and Machine Learning for Network Change Risk Prediction.

---

# License

This project is licensed under the MIT License.
