# Release Readiness Scorecard — Demo Guide

## 1. Problem

Software release decisions depend on multiple quality signals such as test pass rate, defects, coverage, and unresolved risks. Reviewing these signals independently can make release decisions slower and less consistent.

The Release Readiness Scorecard provides a consolidated view of these signals and identifies the modules that are blocking a release.

## 2. Solution Flow

The application follows this workflow:

CSV Upload
→ Data Validation
→ Readiness Score Calculation
→ Release Gates
→ GO / NO-GO Decision
→ Blocker Identification
→ AI Narrative

The release decision is deterministic. AI is used only to explain the already-calculated decision.

## 3. Demo Steps

### Step 1 — Upload Release Data

Upload:

`data/release_metrics.csv`

The application validates the required columns and input ranges.

### Step 2 — Review Release KPIs

The dashboard displays:

- Overall Readiness Score
- Release Decision
- Total Modules
- NO-GO Modules
- Critical Defects
- Unresolved Risks

### Step 3 — Review Release Blockers

The application identifies modules that fail one or more release gates.

For the sample dataset, important problem areas include:

- Payment
- Orders
- Offers
- Reports

### Step 4 — Review Score Breakdown

The readiness score is divided into:

- Test Quality — 30%
- Defect Health — 30%
- Coverage — 20%
- Risk Health — 20%

### Step 5 — Configure Release Gates

The sidebar allows the release engineer to configure:

- Minimum Test Pass %
- Minimum Coverage %
- Minimum Readiness Score
- Maximum Critical Defects

Changing these thresholds recalculates the release decisions.

### Step 6 — Generate AI Narrative

Click:

`Generate Release Narrative`

The AI generates a concise engineering explanation based on the calculated score, decision, blockers, defects, and risks.

The AI does not calculate or override the release decision.

### Step 7 — Export Scorecard

The detailed module-level scorecard can be downloaded as a CSV for further review.

## 4. Demo Talking Points

During the demonstration, explain the workflow in this order:

1. Problem
2. Requirements
3. Architecture
4. Deterministic scoring
5. Release gates
6. Blocker identification
7. Dashboard
8. AI narrative
9. Testing evidence
10. Limitations and future improvements

## 5. Key Design Principle

The core release decision is deterministic and explainable.

AI is intentionally limited to narrative generation so that the AI layer cannot independently approve or reject a software release.

## 6. Prototype Limitations

The current prototype uses:

- CSV input instead of live engineering systems
- Configurable prototype thresholds
- No Jira integration
- No CI/CD integration
- No database or historical release tracking
- No automated deployment or rollback

These items were intentionally kept outside the hackathon scope so that the core release-readiness workflow could be completed and tested end-to-end.

## 7. Future Improvements

Possible production extensions include:

- Jira integration
- CI/CD integration
- Historical release tracking
- Database storage
- Automated notifications
- Authentication and role-based access
- Configurable scoring profiles
- Integration with automated test systems