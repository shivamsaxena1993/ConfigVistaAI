# ConfigVista AI - Risk Evaluation Engine

## Technical Design Document

**Version:** 2.0 (Artifact-1)

**Author:** Shivam Saxena

---

# 1. Overview

The Risk Evaluation Engine estimates the operational impact of Cisco IOS configuration changes.

The current implementation uses a deterministic rule-based approach that assigns a risk label, confidence score and engineering recommendation based on the detected configuration changes.

This implementation serves as the baseline for future Machine Learning models.

---

# 2. Objectives

The Risk Engine performs the following tasks:

- Evaluate every detected configuration change
- Assign operational risk
- Calculate confidence score
- Generate recommendations
- Produce overall assessment statistics

---

# 3. Evaluation Pipeline

```
Configuration Change

        │

        ▼

Change Classification

        ▼

Risk Rules

        ▼

Risk Score

        ▼

Confidence Score

        ▼

Recommendation

        ▼

Overall Assessment
```

---

# 4. Risk Categories

The engine currently supports three risk levels.

| Risk | Score |
|------|------:|
| Low | 0–30 |
| Medium | 31–60 |
| High | 61–100 |

---

# 5. Rule-based Evaluation

Current implementation evaluates risk using engineering rules.

Examples

| Configuration Area | Risk |
|--------------------|------|
| Interface Description | Low |
| Interface MTU | Medium |
| Interface Shutdown | Medium |
| VLAN | Medium |
| OSPF | High |
| BGP | High |
| Static Route | High |
| ACL | High |
| AAA | High |

---

# 6. Confidence Score

The confidence score indicates how certain the rule engine is about the assigned risk.

Typical values

| Category | Confidence |
|----------|-----------:|
| Interface | 90 |
| Routing | 95 |
| Security | 95 |
| Switching | 90 |
| Management | 85 |
| Services | 85 |
| System | 80 |

Higher confidence indicates stronger engineering certainty.

---

# 7. Recommendation Generation

Each evaluated change produces an engineering recommendation.

Example

| Category | Recommendation |
|----------|----------------|
| Routing | Validate routing convergence before deployment. |
| Security | Review access policies and rollback procedures. |
| Interface | Verify interface connectivity after implementation. |
| Switching | Validate VLAN and trunk configuration. |
| Management | Confirm monitoring systems remain operational. |

---

# 8. Overall Risk

The engine calculates an overall assessment using:

- Highest detected risk
- Average risk score
- Number of changes
- Category summary

Outputs include:

- Overall Risk
- Average Risk Score
- Confidence
- Category Summary

---

# 9. Current Architecture

```
Configuration Changes

          │

          ▼

Rule Engine

          ▼

Risk Score

          ▼

Confidence Score

          ▼

Recommendations

          ▼

Executive Summary
```

---

# 10. Current Limitations

Current implementation:

- Rule-based only
- Static engineering rules
- No historical learning
- No probabilistic inference

---

# 11. Future Machine Learning Integration

The next dissertation phase will replace the deterministic engine with supervised learning models.

Planned workflow

```
Configuration Changes

        │

        ▼

Feature Engineering

        ▼

Training Dataset

        ▼

Random Forest

        ▼

XGBoost

        ▼

Model Evaluation

        ▼

SHAP Explainability

        ▼

Hybrid Risk Prediction
```

Future outputs

- Predicted Risk
- Prediction Probability
- Feature Importance
- SHAP Values
- Confidence Interval

---

# 12. Summary

The current Rule-based Risk Evaluation Engine provides a transparent and explainable baseline for assessing Cisco IOS configuration changes.

Its outputs establish the benchmark against which future Machine Learning models will be evaluated as part of the dissertation research.