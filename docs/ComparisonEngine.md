# ConfigVista AI - Comparison Engine

## Technical Design Document

**Version:** 2.0 (Artifact-1)

**Author:** Shivam Saxena

---

# 1. Overview

The Comparison Engine is the core component of ConfigVista AI.

Its primary objective is to compare a baseline Cisco IOS configuration against a candidate configuration while preserving the hierarchical context of Cisco CLI syntax.

Unlike traditional text-based comparison tools, the Comparison Engine understands parent-child relationships within Cisco configurations and evaluates changes in their operational context.

---

# 2. Objectives

The Comparison Engine performs the following tasks:

- Normalize Cisco IOS configurations
- Preserve hierarchical relationships
- Detect Added, Removed and Modified changes
- Maintain parent section context
- Classify networking changes
- Forward changes for risk evaluation

---

# 3. Processing Pipeline

```
Baseline Configuration

        +

Candidate Configuration

        │

        ▼

Normalization

        ▼

Section Mapping

        ▼

Context-aware Parsing

        ▼

Hierarchical Diff Engine

        ▼

Configuration Changes

        ▼

Change Classification

        ▼

Risk Evaluation

        ▼

Report Generation
```

---

# 4. Processing Stages

## Stage 1 – Configuration Normalization

Purpose

Convert configurations into a consistent format before comparison.

Operations performed:

- Remove blank lines
- Remove comments
- Ignore unsupported commands
- Normalize indentation
- Collapse multiline banners
- Remove unnecessary whitespace

Output

Normalized configuration list.

---

## Stage 2 – Context-aware Parsing

The parser builds hierarchical relationships.

Example

```
interface GigabitEthernet0/0

 ip address 10.1.1.1 255.255.255.0

 shutdown
```

Parent Section

```
interface GigabitEthernet0/0
```

Child Commands

```
ip address

shutdown
```

The parser stores:

- Parent Section
- Parent Type
- Child Commands

---

## Stage 3 – Hierarchical Diff Engine

The Diff Engine compares both normalized configurations.

Supported change types

- Added
- Removed
- Modified

Unlike a traditional line-based diff, the engine preserves parent context.

Example

Baseline

```
ip address 10.1.1.1
```

Candidate

```
ip address 10.1.2.1
```

Result

Modified

instead of

Removed

Added

---

## Stage 4 – Change Classification

Detected changes are categorized into engineering domains.

Supported categories

| Parent Type | Category |
|--------------|----------|
| interface | Interface |
| ospf | Routing |
| bgp | Routing |
| eigrp | Routing |
| acl | Security |
| vlan | Switching |
| snmp | Management |
| ntp | Management |
| banner | System |
| hostname | System |

---

## Stage 5 – Risk Evaluation

Each classified change is passed to the Risk Evaluation Engine.

Outputs include:

- Risk Label
- Risk Score
- Confidence Score
- Recommendation

---

# 5. Comparison Models

Each detected change is represented using the following attributes.

| Field | Description |
|--------|-------------|
| Change Type | Added / Removed / Modified |
| Parent Section | Full Cisco parent command |
| Parent Type | Interface / OSPF / ACL etc. |
| Category | Engineering category |
| Risk Level | Low / Medium / High |
| Risk Score | 0–100 |
| Confidence | 0–100 |
| Recommendation | Engineering guidance |

---

# 6. Engineering Advantages

Compared with traditional text comparison, the ConfigVista AI Comparison Engine provides:

- Hierarchical awareness
- Cisco-specific parsing
- Context preservation
- Intelligent change classification
- Structured comparison results
- Integration with risk prediction

---

# 7. Current Limitations

Current implementation:

- Rule-based comparison
- Cisco IOS syntax only
- Configuration snapshots only

Future work:

- Multi-vendor support
- Semantic configuration comparison
- Configuration dependency analysis
- Live SSH collection
- ML-assisted change detection

---

# 8. Summary

The Comparison Engine forms the foundation of ConfigVista AI.

It transforms raw configuration files into structured engineering knowledge that can be evaluated, visualized and eventually processed by Machine Learning models.