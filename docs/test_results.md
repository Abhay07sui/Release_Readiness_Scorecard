# Release Readiness Scorecard — Test Results

## 1. Purpose

This document records the execution results of the test cases defined in `test_cases.md`.

The results are intended to provide evidence that the core release-readiness workflow was tested using positive, negative, boundary, configuration, integration, and AI scenarios.

---

## 2. Test Execution Summary

| Category | Planned Tests | Passed | Failed | Not Executed |
|---|---:|---:|---:|---:|
| Functional | 13 | 0 | 0 | 13 |
| Negative | 9 | 0 | 0 | 9 |
| Boundary | 6 | 0 | 0 | 6 |
| Configuration | 4 | 0 | 0 | 4 |
| AI Integration | 5 | 0 | 0 | 5 |
| Integration | 5 | 0 | 0 | 5 |
| **Total** | **42** | **0** | **0** | **42** |

> The results in this document should be updated after executing each test scenario. Tests should only be marked PASS when the observed result matches the expected result.

---

## 3. Functional Test Results

| Test ID | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| TC01 | Valid CSV processed | `test.py` processed all 12 modules successfully | PASS | Terminal output |
| TC02 | Readiness score calculated | Readiness scores calculated for all 12 modules | PASS | Terminal output |
| TC03 | Defect health calculated | Not executed | NOT EXECUTED | |
| TC04 | Risk health calculated | Not executed | NOT EXECUTED | |
| TC05 | Healthy module marked GO | Healthy modules such as Login and Profile were marked GO | PASS | Terminal output |
| TC06 | Critical defect causes NO-GO | Payment, Orders, and Reports with critical defects were marked NO-GO | PASS | Terminal output |
| TC07 | Low test pass causes NO-GO | Offers with 89% test pass was marked NO-GO | PASS | Terminal output |
| TC08 | Low coverage causes NO-GO | Offers with 79% coverage was marked NO-GO | PASS | Terminal output |
---

## 4. Negative Test Results

| Test ID | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| NT01 | Missing required column | `Coverage_Percentage` removed | Validation error generated | PASS |
| NT02 | Test pass percentage above 100 | `Test_Pass_Percentage = 120` | Validation error generated | PASS |
| NT03 | Negative critical defects | `Critical_Defects = -1` | Validation error generated | PASS |


### Executed Negative Validation Tests

The scoring engine was tested with invalid input conditions to verify that data validation prevents incorrect release calculations.

- Missing required column was rejected.
- Test pass percentage above 100 was rejected.
- Negative critical defect count was rejected.

All three negative validation tests passed successfully.
---

## 5. Boundary Test Results

| Test ID | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| BT01 | Exact release thresholds | Test Pass = 90%, Coverage = 80% | GO | PASS |
| BT02 | Test pass just below threshold | Test Pass = 89.9%, Coverage = 80% | NO-GO | PASS |
| BT03 | Coverage just below threshold | Test Pass = 90%, Coverage = 79.9% | NO-GO | PASS |


### Executed Boundary Tests

The release-gate logic was tested at the exact configured thresholds and immediately below them.

- At the exact minimum thresholds, the release was marked GO.
- A test pass rate of 89.9% resulted in NO-GO.
- Coverage of 79.9% resulted in NO-GO.

This confirms that the configured release gates are enforced correctly at boundary conditions.
---

## 6. Configuration Test Results

| Test ID | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| CG01 | Default gates | 8 GO / 4 NO-GO | PASS |
| CG02 | Minimum Test Pass = 95% | 4 GO / 8 NO-GO | PASS |
| CG03 | Maximum Critical Defects = 1 | 9 GO / 3 NO-GO | PASS |
| CG04 | Minimum Readiness Score = 90 | 7 GO / 5 NO-GO | PASS |

---

## 7. AI Test Results

### Executed AI Narrative Test

| ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| AI01 | Generate release narrative for NO-GO release | Narrative explains the existing decision using calculated metrics and blockers | Narrative generated successfully and matched the NO-GO decision | PASS |

The AI narrative was verified to explain the existing deterministic release decision without changing the calculated GO/NO-GO result.

---


## Testing Summary

The following major areas were executed and verified:

| Area | Result |
|---|---|
| Valid CSV processing | PASS |
| Invalid input validation | PASS |
| Boundary-condition testing | PASS |
| Configurable release gates | PASS |
| AI release narrative | PASS |
| Streamlit end-to-end workflow | PASS |

The core release-readiness workflow was validated from CSV upload through deterministic scoring, GO/NO-GO decision, blocker identification, and AI-generated explanation.