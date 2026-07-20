# ConfigVista AI - User Manual

## Intelligent Network Change Risk Prediction & Decision Support Framework

**Version:** MVP 1.0

**Author:** Shivam Saxena

---

# 1. Introduction

ConfigVista AI is an intelligent decision support framework designed to help network engineers assess the operational risk of Cisco IOS configuration changes before deployment.

The application analyzes network configurations, extracts networking features, predicts change risk, generates implementation recommendations, and stores assessment history within a centralized knowledge base.

---

# 2. System Requirements

- Python 3.13+
- Windows 10/11
- Streamlit
- SQLAlchemy
- SQLite

---

# 3. Starting the Application

Activate the virtual environment.

```bash
venv\Scripts\activate
```

Launch the application.

```bash
streamlit run streamlit_app.py
```

The application opens automatically in your default browser.

---

# 4. Dashboard Overview

The dashboard contains two primary sections:

## Run Assessment

Allows engineers to upload Cisco configuration files for analysis.

## AI Knowledge Base

Displays previously stored assessments and recommendations.

---

# 5. Running an Assessment

### Step 1

Open the **Run Assessment** tab.

---

### Step 2

Upload a Cisco IOS configuration file.

Supported formats:

- .txt
- .cfg
- .conf

---

### Step 3

The system automatically performs:

- Configuration Parsing
- Feature Extraction
- Risk Prediction
- Recommendation Generation
- Assessment Storage

---

### Step 4

Review the generated sections:

- Assessment Summary
- Configuration Overview
- Risk Assessment
- Explainable AI
- Recommendations
- Assessment Workflow

---

# 6. Understanding the Risk Score

Risk Score ranges from 0 to 100.

| Score | Risk |
|---------|------|
| 0 – 30 | Low |
| 31 – 60 | Medium |
| 61 – 100 | High |

The confidence score indicates the certainty of the current rule-based prediction.

---

# 7. Recommendation Categories

Recommendations are grouped into:

- Pre-Checks
- Implementation
- Post Validation
- Monitoring
- Rollback

These provide operational guidance for network engineers during the change lifecycle.

---

# 8. AI Knowledge Base

The Knowledge Base stores historical assessments including:

- Change Reference
- Risk Label
- Confidence Score
- Features
- Recommendations
- Assessment Timestamp

Historical assessments can be reviewed for future analysis.

---

# 9. Troubleshooting

## Database Missing

Run:

```bash
python -m database.initialize_db
```

---

## Database Empty

Run:

```bash
python -m database.seed_data
```

---

## Module Import Errors

Verify the virtual environment is activated.

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Streamlit Not Opening

Verify Streamlit installation.

```bash
streamlit --version
```

---

# 10. Current MVP Limitations

Current implementation includes:

- Rule-based risk engine
- SQLite database
- Cisco IOS parser
- Sample configurations

Current implementation does not yet include:

- Live SSH integration
- Machine Learning
- LLM recommendations
- RAG
- LangSmith tracing

These features are planned for subsequent dissertation phases.

---

# 11. Future Enhancements

Future work includes:

- Random Forest Risk Prediction
- XGBoost Classification
- Explainable ML
- RAG-based Recommendation Engine
- Live Device Integration
- Human-in-the-Loop Approval
- LangSmith Observability
- Continuous Learning

---

# 12. Contact

Author

Shivam Saxena

MSc Dissertation

ConfigVista AI