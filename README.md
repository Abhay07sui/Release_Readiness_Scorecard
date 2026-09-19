# 🚀 Release Readiness Scorecard

A lightweight engineering-quality dashboard that evaluates whether a software release is ready to ship based on test quality, defects, test coverage, and unresolved risks.

The system processes release metrics from a CSV file, calculates a readiness score for each module, applies configurable release gates, identifies release blockers, and optionally uses AI to generate a concise engineering narrative explaining the calculated decision.

---

## 🎯 Problem Statement

Software release decisions often depend on multiple quality signals such as:

- Test pass percentage
- Critical defects
- High-severity defects
- Test coverage
- Unresolved risks

These signals are often reviewed separately, making it difficult to quickly determine:

1. How healthy the release is overall
2. Which modules are creating release risk
3. Whether the release satisfies minimum quality gates
4. Why the release received a GO or NO-GO decision

The Release Readiness Scorecard combines these signals into a single, explainable release-readiness view.

---

## 💡 Solution

The application:

1. Accepts release metrics through a CSV file
2. Validates the input data
3. Calculates health metrics for each module
4. Calculates an overall readiness score
5. Applies configurable release gates
6. Produces a GO / NO-GO decision
7. Identifies release blockers
8. Displays visual quality dashboards
9. Generates an AI-assisted narrative explaining the existing decision
10. Allows the processed scorecard to be downloaded as CSV

---

## 🏗️ Project Architecture

```text
                    CSV INPUT
                        │
                        ▼
              ┌───────────────────┐
              │   Data Validation │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Score Calculation │
              │                   │
              │ Test Quality 30%  │
              │ Defect Health 30% │
              │ Coverage 20%      │
              │ Risk Health 20%   │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  Release Gates    │
              │                   │
              │ Test Pass         │
              │ Coverage          │
              │ Readiness Score   │
              │ Critical Defects  │
              └─────────┬─────────┘
                        │
                 ┌──────┴──────┐
                 ▼             ▼
                GO           NO-GO
                               │
                               ▼
                       Release Blockers
                               │
                               ▼
                         AI Narrative