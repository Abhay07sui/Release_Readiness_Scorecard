import streamlit as st
import pandas as pd
import plotly.express as px

from scoring import process_release_data
from ai_narrative import generate_release_narrative


# Page configuration
st.set_page_config(
    
    page_title="Release Readiness Scorecard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# RELEASE GATE SETTINGS
# ==========================================

with st.sidebar:

    st.header("⚙️ Release Gates")

    st.write(
        "Configure the minimum quality thresholds "
        "used for the GO / NO-GO decision."
    )

    min_test_pass = st.slider(
        "Minimum Test Pass %",
        min_value=0,
        max_value=100,
        value=90,
        step=1
    )

    min_coverage = st.slider(
        "Minimum Coverage %",
        min_value=0,
        max_value=100,
        value=80,
        step=1
    )

    min_readiness_score = st.slider(
        "Minimum Readiness Score",
        min_value=0,
        max_value=100,
        value=80,
        step=1
    )

    max_critical_defects = st.number_input(
        "Maximum Critical Defects",
        min_value=0,
        max_value=20,
        value=0,
        step=1
    )

    st.divider()

    st.caption("Current release gates")

    st.write(
        f"Test Pass ≥ **{min_test_pass}%**"
    )

    st.write(
        f"Coverage ≥ **{min_coverage}%**"
    )

    st.write(
        f"Readiness Score ≥ **{min_readiness_score}**"
    )

    st.write(
        f"Critical Defects ≤ **{max_critical_defects}**"
    )
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.7rem !important;
    margin-top: 1.5rem !important;
}

[data-testid="stMetric"] {
    background-color: #151922;
    border: 1px solid #303642;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem;
}

</style>
""", unsafe_allow_html=True)


# Title
st.title("🚀 Release Readiness Scorecard")
st.info(
    "The readiness score measures overall release health. "
    "GO / NO-GO is determined separately using the configured "
    "release gates in the sidebar."
)

st.markdown(
    "Evaluate software release readiness using **test quality, "
    "defects, coverage, and unresolved risks**."
)

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Release Metrics CSV",
    type=["csv"]
)


# Process uploaded file
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    try:

        df = process_release_data(
    df,
    min_test_pass=min_test_pass,
    min_coverage=min_coverage,
    min_readiness_score=min_readiness_score,
    max_critical_defects=max_critical_defects
)

        st.success("CSV processed successfully!")

        # Overall release decision
        
        # =========================
        # OVERALL RELEASE STATUS
        # =========================

        overall_decision = (
            "NO-GO"
            if (df["Decision"] == "NO-GO").any()
            else "GO"
        )

        # Overall readiness score
        overall_score = df["Readiness_Score"].mean()

        # Score breakdown
        test_quality = df["Test_Pass_Percentage"].mean() * 0.30
        defect_health = df["Defect_Health"].mean() * 0.30
        coverage_score = df["Coverage_Percentage"].mean() * 0.20
        risk_health = df["Risk_Health"].mean() * 0.20

        total_modules = len(df)

        no_go_modules = (df["Decision"] == "NO-GO").sum()

        critical_defects = df["Critical_Defects"].sum()

        unresolved_risks = df["Unresolved_Risks"].sum()


        # =========================
        # KPI CARDS
        # =========================

        st.subheader("Release Overview")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric(
                "Readiness Score",
                f"{overall_score:.1f}/100"
            )

        with col2:
            st.metric(
                "Release Decision",
                overall_decision
            )

        with col3:
            st.metric(
                "Total Modules",
                total_modules
            )

        with col4:
            st.metric(
                "NO-GO Modules",
                no_go_modules
            )

        with col5:
            st.metric(
                "Critical Defects",
                int(critical_defects)
            )

        with col6:
            st.metric(
                "Unresolved Risks",
                int(unresolved_risks)
            )

        st.subheader("📌 Release Summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.metric(
                "Average Test Pass",
                f"{df['Test_Pass_Percentage'].mean():.1f}%"
            )

        with summary_col2:
            st.metric(
                "Average Coverage",
                f"{df['Coverage_Percentage'].mean():.1f}%"
            )

        with summary_col3:
            st.metric(
                "Average Readiness",
                f"{df['Readiness_Score'].mean():.1f}/100"
            )            

        #===================================================
        st.subheader("📊 Readiness Score Breakdown")

        breakdown_col1, breakdown_col2, breakdown_col3, breakdown_col4 = st.columns(4)

        with breakdown_col1:
            st.metric(
                "Test Quality",
                f"{test_quality:.1f}/30"
            )

        with breakdown_col2:
            st.metric(
                "Defect Health",
                f"{defect_health:.1f}/30"
            )

        with breakdown_col3:
            st.metric(
                "Coverage",
                f"{coverage_score:.1f}/20"
            )

        with breakdown_col4:
            st.metric(
                "Risk Health",
                f"{risk_health:.1f}/20"
            )

        st.caption(
            "Score = Test Quality (30%) + Defect Health (30%) "
            "+ Coverage (20%) + Risk Health (20%)."
)
        #

        if overall_decision == "GO":
            st.success("✅ Release is ready based on the configured readiness gates.")
        else:
            st.error(
                "🚫 Release is not ready. One or more modules "
                "failed the configured readiness gates.")    

        # =========================
        # RELEASE BLOCKERS
        # =========================

        st.subheader("🚨 Release Blockers")

        blocked_modules = (df[df["Decision"] == "NO-GO"].sort_values("Readiness_Score", ascending=True))
        if len(blocked_modules) == 0:

            st.success("No release blockers detected.")

        else:

            for _, row in blocked_modules.iterrows():

                st.warning(
                    f"**{row['Module']}** — "
                    f"{'; '.join(row['Reasons'])}"
                )  

        # =========================
        # AI RELEASE NARRATIVE
        # =========================

        st.subheader("🤖 AI Release Narrative")

        if st.button("Generate Release Narrative"):

            with st.spinner("Generating release analysis..."):

                narrative = generate_release_narrative(
                    overall_score=overall_score,
                    overall_decision=overall_decision,
                    blocked_modules=blocked_modules,
                    critical_defects=critical_defects,
                    unresolved_risks=unresolved_risks
                )

            st.info(narrative)       

        #===========================================
        # MODULE READINESS SCORE
        # ==========================================

        st.subheader("📊 Module Readiness Score")

        score_chart = (
            df[
                ["Module", "Readiness_Score"]
            ]
            .sort_values("Readiness_Score", ascending=True)
        )

        fig_score = px.bar(
            score_chart,
            x="Readiness_Score",
            y="Module",
            orientation="h",
            text="Readiness_Score",
            range_x=[0, 100],
            labels={
                "Readiness_Score": "Readiness Score",
                "Module": "Module"
            }
        )

        fig_score.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

        fig_score.update_layout(
            height=500,
            margin=dict(l=20, r=40, t=20, b=20),
            xaxis=dict(
                range=[0, 100]
            )
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )

        # ==========================================
        # TEST PASS VS COVERAGE
        # ==========================================

        st.subheader("🧪 Test Pass Rate vs Coverage")

        quality_data = df[
            [
                "Module",
                "Test_Pass_Percentage",
                "Coverage_Percentage"
            ]
        ].sort_values(
            "Test_Pass_Percentage",
            ascending=True
        )

        quality_long = quality_data.melt(
            id_vars="Module",
            value_vars=[
                "Test_Pass_Percentage",
                "Coverage_Percentage"
            ],
            var_name="Metric",
            value_name="Percentage"
        )

        quality_long["Metric"] = quality_long["Metric"].replace({
            "Test_Pass_Percentage": "Test Pass %",
            "Coverage_Percentage": "Coverage %"
        })

        fig_quality = px.bar(
            quality_long,
            x="Module",
            y="Percentage",
            color="Metric",
            barmode="group",
            text="Percentage",
            range_y=[0, 100],
            labels={
                "Percentage": "Percentage",
                "Module": "Module"
            }
        )

        fig_quality.update_traces(
            texttemplate="%{text:.0f}%",
            textposition="outside"
        )

        fig_quality.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=100),
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig_quality,
            use_container_width=True
        )

        # ==========================================
        # DEFECTS AND RISKS
        # ==========================================

        st.subheader("🚨 Defects & Risks by Module")

        risk_data = (
            df[
                [
                    "Module",
                    "Critical_Defects",
                    "High_Defects",
                    "Unresolved_Risks"
                ]
            ]
            .sort_values(
                "Unresolved_Risks",
                ascending=False
            )
        )

        risk_long = risk_data.melt(
            id_vars="Module",
            value_vars=[
                "Critical_Defects",
                "High_Defects",
                "Unresolved_Risks"
            ],
            var_name="Signal",
            value_name="Count"
        )

        risk_long["Signal"] = risk_long["Signal"].replace({
            "Critical_Defects": "Critical Defects",
            "High_Defects": "High Defects",
            "Unresolved_Risks": "Unresolved Risks"
        })

        fig_risk = px.bar(
            risk_long,
            x="Module",
            y="Count",
            color="Signal",
            barmode="stack",
            text="Count",
            labels={
                "Count": "Count",
                "Module": "Module"
            }
        )

        fig_risk.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=100),
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ==========================================
        # DETAILED SCORECARD
        # ==========================================

        st.subheader("📋 Detailed Module Scorecard")

        display_df = df[
            [
                "Module",
                "Test_Pass_Percentage",
                "Critical_Defects",
                "High_Defects",
                "Coverage_Percentage",
                "Unresolved_Risks",
                "Defect_Health",
                "Risk_Health",
                "Readiness_Score",
                "Decision",
                "Reasons"
            ]
        ].copy()

        display_df = display_df.rename(columns={
            "Test_Pass_Percentage": "Test Pass %",
            "Critical_Defects": "Critical",
            "High_Defects": "High",
            "Coverage_Percentage": "Coverage %",
            "Unresolved_Risks": "Risks",
            "Defect_Health": "Defect Health",
            "Risk_Health": "Risk Health",
            "Readiness_Score": "Readiness",
            "Decision": "Decision",
            "Reasons": "Reasons"
        })

        display_df = display_df.sort_values(
            "Readiness",
            ascending=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Module": st.column_config.TextColumn(
                    "Module",
                    width="medium"
                ),

                "Test Pass %": st.column_config.NumberColumn(
                    "Test Pass %",
                    format="%.0f%%"
                ),

                "Critical": st.column_config.NumberColumn(
                    "Critical",
                    format="%d"
                ),

                "High": st.column_config.NumberColumn(
                    "High",
                    format="%d"
                ),

                "Coverage %": st.column_config.NumberColumn(
                    "Coverage %",
                    format="%.0f%%"
                ),

                "Risks": st.column_config.NumberColumn(
                    "Risks",
                    format="%d"
                ),

                "Defect Health": st.column_config.NumberColumn(
                    "Defect Health",
                    format="%.0f"
                ),

                "Risk Health": st.column_config.NumberColumn(
                    "Risk Health",
                    format="%.0f"
                ),

                "Readiness": st.column_config.NumberColumn(
                    "Readiness",
                    format="%.1f"
                ),

                "Decision": st.column_config.TextColumn(
                    "Decision",
                    width="small"
                ),

                "Reasons": st.column_config.TextColumn(
                    "Reasons",
                    width="large"
                )
            }
        )

        # Download processed scorecard
        csv_data = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Scorecard CSV",
            data=csv_data,
            file_name="release_readiness_scorecard.csv",
            mime="text/csv"
        )
        

    except ValueError as e:

        st.error(str(e))

