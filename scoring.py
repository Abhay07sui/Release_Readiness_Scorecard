import pandas as pd


# =========================
# INPUT VALIDATION
# =========================

def validate_data(df):

    required_columns = [
        "Module",
        "Test_Pass_Percentage",
        "Critical_Defects",
        "High_Defects",
        "Coverage_Percentage",
        "Unresolved_Risks"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check missing values
    if df[required_columns].isnull().any().any():
        raise ValueError(
            "CSV contains missing values in required columns."
        )

    # Check test pass percentage
    if not df["Test_Pass_Percentage"].between(0, 100).all():
        raise ValueError(
            "Test_Pass_Percentage must be between 0 and 100."
        )

    # Check coverage percentage
    if not df["Coverage_Percentage"].between(0, 100).all():
        raise ValueError(
            "Coverage_Percentage must be between 0 and 100."
        )

    # Check defects and risks
    if (df["Critical_Defects"] < 0).any():
        raise ValueError(
            "Critical_Defects cannot be negative."
        )

    if (df["High_Defects"] < 0).any():
        raise ValueError(
            "High_Defects cannot be negative."
        )

    if (df["Unresolved_Risks"] < 0).any():
        raise ValueError(
            "Unresolved_Risks cannot be negative."
        )

    return True


# =========================
# SCORING ENGINE
# =========================

def calculate_scores(df):

    # Defect Health
    df["Defect_Health"] = (
        100
        - df["Critical_Defects"] * 20
        - df["High_Defects"] * 5
    ).clip(lower=0)

    # Risk Health
    df["Risk_Health"] = (
        100
        - df["Unresolved_Risks"] * 10
    ).clip(lower=0)

    # Overall Readiness Score
    df["Readiness_Score"] = (
        df["Test_Pass_Percentage"] * 0.30
        + df["Defect_Health"] * 0.30
        + df["Coverage_Percentage"] * 0.20
        + df["Risk_Health"] * 0.20
    )

    # Round score
    df["Readiness_Score"] = df["Readiness_Score"].round(1)

    return df


# =========================
# GO / NO-GO DECISION
# =========================

def check_release_readiness(
    row,
    min_test_pass=90,
    min_coverage=80,
    min_readiness_score=80,
    max_critical_defects=0
):

    reasons = []

    critical = row["Critical_Defects"]
    test_pass = row["Test_Pass_Percentage"]
    coverage = row["Coverage_Percentage"]
    score = row["Readiness_Score"]

    # Gate 1: Critical defects
    if critical > max_critical_defects:
        reasons.append(
            f"{critical} critical defect(s) detected "
            f"(maximum allowed: {max_critical_defects})"
        )

    # Gate 2: Test pass percentage
    if test_pass < min_test_pass:
        reasons.append(
            f"Test pass rate is {test_pass}% "
            f"(minimum {min_test_pass}%)"
        )

    # Gate 3: Coverage
    if coverage < min_coverage:
        reasons.append(
            f"Coverage is {coverage}% "
            f"(minimum {min_coverage}%)"
        )

    # Gate 4: Overall score
    if score < min_readiness_score:
        reasons.append(
            f"Readiness score is {score:.1f} "
            f"(minimum {min_readiness_score})"
        )

    # Final decision
    if len(reasons) == 0:
        decision = "GO"
    else:
        decision = "NO-GO"

    return decision, reasons

# =========================
# COMPLETE PIPELINE
# =========================


def process_release_data(
    df,
    min_test_pass=90,
    min_coverage=80,
    min_readiness_score=80,
    max_critical_defects=0
):

    # Validate input
    validate_data(df)

    # Calculate scores
    df = calculate_scores(df)

    # Calculate GO / NO-GO decision
    df[["Decision", "Reasons"]] = df.apply(
        lambda row: pd.Series(
            check_release_readiness(
                row,
                min_test_pass=min_test_pass,
                min_coverage=min_coverage,
                min_readiness_score=min_readiness_score,
                max_critical_defects=max_critical_defects
            )
        ),
        axis=1
    )

    return df