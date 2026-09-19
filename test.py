import pandas as pd

from scoring import process_release_data


# Read CSV
df = pd.read_csv("data/release_metrics.csv")


# Process release data
df = process_release_data(df)


# Display results
print(
    df[
        [
            "Module",
            "Readiness_Score",
            "Decision",
            "Reasons"
        ]
    ]
)