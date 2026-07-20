# ConfigVista AI

**An Intelligent Network Configuration Change Risk Assessment Framework**

ConfigVista AI is an AI-assisted network configuration analysis platform developed as part of a Master's dissertation. The system automates configuration comparison, classifies network changes, evaluates implementation risk, and generates detailed reports to assist network engineers during change management.

---

# Project Overview

Network changes are one of the leading causes of service outages in enterprise environments. Manual configuration review is time-consuming, error-prone, and difficult to scale.

ConfigVista AI addresses this challenge by providing an intelligent framework that:

- Compares baseline and candidate configurations
- Detects configuration changes
- Classifies changes by technology domain
- Estimates implementation risk
- Generates comprehensive comparison reports
- Provides an interactive Streamlit dashboard

The current implementation focuses on Cisco IOS-style configurations.

---

# Features

## Configuration Comparison

- Context-aware configuration comparison
- Parent section detection
- Line-by-line change tracking
- Added / Removed / Modified detection

Supported configuration sections include:

- Interfaces
- Routing
- Security
- VLANs
- Services
- Management

---

## Intelligent Change Classification

Automatically categorizes configuration changes into:

- Interface
- Routing
- Switching
- Security
- Services
- Management

---

## Risk Evaluation

Rule-based risk assessment provides:

- Risk Level
    - High
    - Medium
    - Low

- Risk Score

- Confidence Score

- Implementation Recommendations

Examples:

| Change | Risk |
|---------|------|
| Interface IP Change | Low |
| Interface Shutdown | Medium |
| OSPF Change | High |
| BGP Change | High |
| ACL Modification | High |
| Default Route Change | High |

---

## Report Generation

Automatically generates reports in multiple formats:

- Text
- Markdown
- HTML
- JSON

Each report includes:

- Executive Summary
- Risk Summary
- Category Summary
- Detailed Change Analysis
- Recommendations

---

## Streamlit Dashboard

Interactive dashboard supports:

- Upload Baseline Configuration
- Upload Candidate Configuration
- Compare Configurations
- Risk Dashboard
- Category Summary
- Detailed Change Explorer
- Report Downloads

---

# Project Architecture

```
                   +----------------------+
                   | Configuration Files  |
                   +----------+-----------+
                              |
                              v
                  +------------------------+
                  | Configuration Parser   |
                  +-----------+------------+
                              |
                              v
                  +------------------------+
                  | Diff Engine            |
                  +-----------+------------+
                              |
                              v
                  +------------------------+
                  | Change Classifier      |
                  +-----------+------------+
                              |
                              v
                  +------------------------+
                  | Risk Evaluator         |
                  +-----------+------------+
                              |
                              v
                  +------------------------+
                  | Comparison Engine      |
                  +-----------+------------+
                              |
              +---------------+----------------+
              |                                |
              v                                v
      Report Generator                Streamlit Dashboard
```

---

# Project Structure

```
ConfigVistaAI/

│
├── comparison/
│   ├── change_classifier.py
│   ├── comparison_engine.py
│   ├── diff_engine.py
│   ├── models.py
│   ├── report_generator.py
│   ├── risk_evaluator.py
│   └── utils.py
│
├── database/
│   ├── schema.sql
│   ├── initialize_db.py
│   ├── seed_data.py
│   └── configvista.db
│
├── reports/
│
├── sample_configs/
│
├── tests/
│   ├── test_diff_engine.py
│   ├── test_change_classifier.py
│   ├── test_risk_evaluator.py
│   └── test_comparison_engine.py
│
├── docs/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

---

# Technology Stack

Programming Language

- Python 3.11+

Libraries

- Streamlit
- Pandas
- SQLite
- difflib
- Dataclasses
- Enum
- JSON

Database

- SQLite

Development Tools

- VS Code
- Git
- GitHub

---

# Installation

Clone the repository

```bash
git clone https://github.com/<username>/ConfigVistaAI.git
```

Move into the project

```bash
cd ConfigVistaAI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Launch the Streamlit dashboard

```bash
streamlit run streamlit_app.py
```

---

# Running Unit Tests

Run Diff Engine tests

```bash
python -m tests.test_diff_engine
```

Run Comparison Engine integration test

```bash
python -m tests.test_comparison_engine
```

Run all tests

```bash
python -m pytest
```

---

# Example Workflow

1. Upload Baseline Configuration

↓

2. Upload Candidate Configuration

↓

3. Compare Configurations

↓

4. Review Risk Assessment

↓

5. Download Reports

---

# Current Project Status

## Phase 1

- Architecture Design
- Database Design
- Project Setup

Completed

---

## Phase 2

- Configuration Parser
- Diff Engine
- Change Classifier
- Risk Evaluator
- Report Generator
- Streamlit Dashboard
- Unit Testing
- Integration Testing

Completed

---

## Phase 3 (Upcoming)

Machine Learning Based Risk Prediction

Planned components:

- Dataset Generation
- Feature Engineering
- Random Forest Model
- XGBoost Model
- Model Evaluation
- Risk Prediction API
- AI-assisted Recommendations

---

# Future Enhancements

- Multi-vendor configuration support
- Juniper and Arista parsers
- Configuration rollback prediction
- Topology-aware change analysis
- Real-time telemetry integration
- Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP) integration
- LLM-assisted recommendation engine

---

# Known Limitations

Current version uses rule-based risk assessment.

Configuration comparison is primarily line-based using Python's SequenceMatcher.

Designed for Cisco IOS-style configurations.

Machine Learning prediction will be introduced in Phase 3.

---

# Dissertation

**Title**

ConfigVista AI: An Intelligent Network Change Risk Prediction and Retrieval-Augmented Decision Support Framework for Network Operations

This project forms part of the MSc dissertation and demonstrates the application of Artificial Intelligence and Machine Learning to network change management.

---

# Author

**Shivam Saxena**

Technical Consulting Engineer

Cisco Systems

Master's Dissertation Project

2026

---

# License

This project is intended for academic research and educational purposes.