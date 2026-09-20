# Release Readiness Scorecard — Test Cases

## 1. Testing Objective

The objective of testing is to verify that the Release Readiness Scorecard correctly:

- Accepts valid release metrics
- Rejects invalid input
- Calculates readiness scores correctly
- Applies release gates correctly
- Identifies release blockers
- Recalculates decisions when thresholds change
- Generates the AI narrative
- Handles AI/API failures gracefully
- Exports the processed scorecard

---

## 2. Testing Approach

Testing covers:

- Functional testing
- Negative testing
- Boundary testing
- Integration testing
- Error handling
- Basic usability verification

The primary focus is on validating the deterministic release-decision logic before validating the dashboard and AI integration.

---

## 3. Test Environment

### Application

Release Readiness Scorecard

### Input

CSV release metrics

### Main Technologies

- Python
- Pandas
- Streamlit
- Plotly
- OpenAI API

---

## 4. Functional Test Cases

| ID | Test Scenario | Test Data / Action | Expected Result |
|---|---|---|---|
| TC01 | Upload valid CSV | Upload valid release_metrics.csv | CSV is processed successfully |
| TC02 | Calculate readiness score | Process valid module metrics | Readiness score is calculated |
| TC03 | Calculate defect health | Critical and high defects provided | Defect health is calculated correctly |
| TC04 | Calculate risk health | Unresolved risks provided | Risk health is calculated correctly |
| TC05 | Healthy module | All release gates satisfied | Module is marked GO |
| TC06 | Critical defect blocker | Critical defects > allowed maximum | Module is marked NO-GO |
| TC07 | Low test pass | Test pass below configured threshold | Module is marked NO-GO |
| TC08 | Low coverage | Coverage below configured threshold | Module is marked NO-GO |
| TC09 | Low readiness score | Score below configured threshold | Module is marked NO-GO |
| TC10 | Multiple blockers | Multiple modules fail gates | All failed modules are identified |
| TC11 | Overall decision | At least one module is NO-GO | Overall release is NO-GO |
| TC12 | Scorecard display | Process valid CSV | Detailed scorecard is displayed |
| TC13 | CSV export | Click Download Scorecard | Processed CSV can be downloaded |

---

## 5. Negative Test Cases

| ID | Test Scenario | Test Data / Action | Expected Result |
|---|---|---|---|
| TC14 | Missing required column | Remove Coverage_Percentage | Validation error |
| TC15 | Missing value | Leave a required metric blank | Validation error |
| TC16 | Test pass > 100 | Set Test Pass to 105 | Validation error |
| TC17 | Test pass < 0 | Set Test Pass to -5 | Validation error |
| TC18 | Coverage > 100 | Set Coverage to 110 | Validation error |
| TC19 | Coverage < 0 | Set Coverage to -5 | Validation error |
| TC20 | Negative critical defects | Set Critical Defects to -1 | Validation error |
| TC21 | Negative high defects | Set High Defects to -1 | Validation error |
| TC22 | Negative unresolved risks | Set Risks to -1 | Validation error |

---

## 6. Boundary Test Cases

| ID | Test Scenario | Test Data / Action | Expected Result |
|---|---|---|---|
| TC23 | Test pass exactly at threshold | Test Pass = 90% | Gate passes |
| TC24 | Coverage exactly at threshold | Coverage = 80% | Gate passes |
| TC25 | Score exactly at threshold | Readiness Score = 80 | Gate passes |
| TC26 | Critical defects at maximum | Critical Defects = 0 | Gate passes |
| TC27 | Test pass just below threshold | Test Pass = 89.9% | Gate fails |
| TC28 | Coverage just below threshold | Coverage = 79.9% | Gate fails |

---

## 7. Configuration Test Cases

| ID | Test Scenario | Test Data / Action | Expected Result |
|---|---|---|---|
| TC29 | Change minimum test pass | Change threshold from 90 to 95 | Module decisions recalculate |
| TC30 | Change coverage threshold | Change threshold from 80 to 90 | Module decisions recalculate |
| TC31 | Change readiness threshold | Change threshold from 80 to 90 | Module decisions recalculate |
| TC32 | Change critical defect limit | Change maximum critical defects | Gate behavior changes accordingly |

---

## 8. AI Integration Test Cases

| ID | Test Scenario | Test Data / Action | Expected Result |
|---|---|---|---|
| TC33 | Generate narrative | Click Generate Release Narrative | Narrative is generated |
| TC34 | Narrative uses existing decision | Existing decision = NO-GO | Narrative explains NO-GO |
| TC35 | AI should not change decision | Provide existing GO/NO-GO result | Decision remains unchanged |
| TC36 | Missing API configuration | Remove/disable API configuration | Friendly error is displayed |
| TC37 | API failure | Simulate unavailable API | Application handles failure without crashing |

---

## 9. Integration Test Cases

| ID | Test Scenario | Expected Result |
|---|---|---|
| TC38 | CSV → validation → scoring | Valid data reaches scoring engine |
| TC39 | Scoring → release gates | Calculated scores are evaluated against configured gates |
| TC40 | Release gates → dashboard | GO/NO-GO and reasons appear correctly |
| TC41 | Dashboard → AI narrative | Calculated results are passed to AI narrative generation |
| TC42 | Full end-to-end workflow | Upload → process → decision → dashboard → narrative works |

---

## 10. Acceptance Criteria Verification

The following acceptance criteria are covered by the test cases:

- Valid CSV is accepted
- Required columns are validated
- Invalid metric ranges are rejected
- Readiness score is calculated
- Release gates are applied
- Failed modules are marked NO-GO
- Blocker reasons are displayed
- Thresholds can be configured
- Decisions update when thresholds change
- AI generates an explanatory narrative
- AI does not change the deterministic release decision

---

## 11. Testing Principle

The core release-decision logic is deterministic and should be validated independently of the AI component.

The AI layer is treated as an explanatory feature rather than a decision-making component.