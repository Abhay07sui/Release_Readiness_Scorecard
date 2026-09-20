# Release Readiness Scorecard — Architecture

## 1. Overview

The Release Readiness Scorecard is a Python-based application that evaluates software release readiness using multiple quality signals.

The application combines:

- Test pass percentage
- Critical defects
- High defects
- Test coverage
- Unresolved risks

The system calculates a deterministic readiness score, evaluates configurable release gates, identifies blockers, and presents the results through an interactive Streamlit dashboard.

An AI component is used only to generate a concise narrative explaining the already-calculated release decision.

---

## 2. High-Level Architecture

```text
                    Release Metrics CSV
                            |
                            v
                   +------------------+
                   |  Streamlit UI    |
                   |  CSV Upload      |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Data Validation  |
                   |    scoring.py    |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Scoring Engine   |
                   |                  |
                   | Test Quality     |
                   | Defect Health    |
                   | Coverage         |
                   | Risk Health      |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Release Gates    |
                   |                  |
                   | GO / NO-GO       |
                   +--------+---------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
        +----------------+    +----------------+
        | Blockers &     |    | Dashboard &    |
        | Reasons        |    | Scorecard      |
        +----------------+    +-------+--------+
                                     |
                                     v
                              +--------------+
                              |  OpenAI API  |
                              | AI Narrative |
                              +--------------+