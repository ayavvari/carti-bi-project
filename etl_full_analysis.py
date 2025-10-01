"""End‑to‑end ETL and analytics for the CARTI healthcare BI project.

This script performs the following:

1. Load synthetic SG2, CRM and EHR data (generated via generate_full_data.py).
2. Integrate and transform the data into a unified analytic dataset.
3. Compute aggregated metrics per provider, including ROI and claim statistics.
4. Train a regression model to predict opportunity value based on provider metrics.
5. Export outputs:
   - A provider summary CSV with actual and predicted values.
   - An Excel file with multiple tabs for Power BI import (SG2, CRM, EHR, Summary).
   - Optional charts illustrating key relationships (patient volume, ROI vs cost, predicted vs actual).

The goal of this script is to demonstrate data engineering, analytics and
predictive modelling capabilities consistent with the CARTI job
description.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt


def load_data():
    """Load the synthetic CSV files into pandas DataFrames."""
    sg2 = pd.read_csv("sg2_patient_flow_full.csv", parse_dates=["admission_date", "discharge_date"])
    crm = pd.read_csv("salesforce_crm_full.csv")
    ehr = pd.read_csv("ehr_data_full.csv", parse_dates=["visit_date"])
    return sg2, crm, ehr


def integrate_data(sg2: pd.DataFrame, crm: pd.DataFrame, ehr: pd.DataFrame) -> pd.DataFrame:
    """Integrate SG2, CRM and EHR data into a provider-level summary.

    Args:
        sg2: Patient flow records with provider names and service lines.
        crm: CRM metrics per provider.
        ehr: EHR visit records with claims information.

    Returns:
        summary: Aggregated metrics for each provider.
    """
    # Aggregate SG2 patient records by provider
    sg2_agg = sg2.groupby("referral_provider").agg(
        total_patients=("patient_id", "count"),
        avg_length_of_stay=("length_of_stay", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        avg_cost=("treatment_cost", "mean"),
    ).reset_index().rename(columns={"referral_provider": "provider_name"})

    # Aggregate EHR claims by provider
    ehr_agg = ehr.groupby("provider_name").agg(
        total_visits=("patient_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        total_claim_paid=("claim_paid", "sum"),
        denial_rate=("claim_status", lambda x: (x == "Denied").mean()),
    ).reset_index()

    # Merge all together on provider name
    merged = sg2_agg.merge(crm, on="provider_name", how="left").merge(ehr_agg, on="provider_name", how="left")

    # Calculate ROI: (deals_value - marketing_cost) / marketing_cost
    merged["roi"] = (merged["deals_value"] - merged["marketing_cost"]) / merged["marketing_cost"]
    # Value per patient
    merged["value_per_patient"] = merged["deals_value"] / merged["total_patients"]
    # Claim collection rate
    merged["claim_collection_rate"] = merged["total_claim_paid"] / merged["total_claim_amount"]

    return merged


def train_predictive_model(summary: pd.DataFrame) -> pd.DataFrame:
    """Train a linear regression model to predict opportunity value.

    Uses provider-level metrics as features to estimate opportunity_value.
    Adds predicted values to the summary DataFrame.
    """
    features = summary[[
        "total_patients", "avg_length_of_stay", "avg_satisfaction",
        "avg_cost", "contact_count", "deals_value", "marketing_cost",
        "total_claim_amount", "total_claim_paid", "denial_rate"
    ]].fillna(0)
    target = summary["opportunity_value"].fillna(0)

    # Create a pipeline with standardization and linear regression
    model = make_pipeline(StandardScaler(), LinearRegression())
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Predictive model evaluation: MAE={mae:.2f}, R2={r2:.2f}")
    # Add predictions for all providers
    summary["predicted_opportunity_value"] = model.predict(features)
    return summary


def export_outputs(sg2: pd.DataFrame, crm: pd.DataFrame, ehr: pd.DataFrame, summary: pd.DataFrame) -> None:
    """Export processed data to CSV and Excel for downstream use.

    Args:
        sg2: Original SG2 patient flow data.
        crm: Original CRM metrics.
        ehr: Original EHR data.
        summary: Provider summary with predictions.
    """
    # Save provider summary
    summary.to_csv("provider_summary_full.csv", index=False)
    # Create Excel workbook with multiple sheets
    with pd.ExcelWriter("carti_full_powerbi_dataset.xlsx", engine="xlsxwriter") as writer:
        sg2.to_excel(writer, sheet_name="SG2_Patient_Flow", index=False)
        crm.to_excel(writer, sheet_name="Salesforce_CRM", index=False)
        ehr.to_excel(writer, sheet_name="EHR_Data", index=False)
        summary.to_excel(writer, sheet_name="Provider_Summary", index=False)
    print("Outputs exported: provider_summary_full.csv, carti_full_powerbi_dataset.xlsx")


def generate_charts(summary: pd.DataFrame) -> None:
    """Generate charts illustrating key metrics and save to files."""
    # Bar chart: ROI per provider
    plt.figure()
    summary_sorted = summary.sort_values("roi")
    plt.barh(summary_sorted["provider_name"], summary_sorted["roi"])
    plt.xlabel("ROI")
    plt.ylabel("Provider")
    plt.title("Return on Investment by Provider")
    plt.tight_layout()
    plt.savefig("roi_by_provider.png")
    plt.close()

    # Scatter: Predicted vs actual opportunity value
    plt.figure()
    plt.scatter(summary["opportunity_value"], summary["predicted_opportunity_value"])
    max_val = max(summary["opportunity_value"].max(), summary["predicted_opportunity_value"].max())
    plt.plot([0, max_val], [0, max_val], linestyle="--")
    plt.xlabel("Actual Opportunity Value")
    plt.ylabel("Predicted Opportunity Value")
    plt.title("Predicted vs Actual Opportunity Value (Per Provider)")
    plt.tight_layout()
    plt.savefig("predicted_vs_actual_opportunity.png")
    plt.close()
    print("Charts generated: roi_by_provider.png, predicted_vs_actual_opportunity.png")


def main():
    sg2, crm, ehr = load_data()
    summary = integrate_data(sg2, crm, ehr)
    summary = train_predictive_model(summary)
    export_outputs(sg2, crm, ehr, summary)
    generate_charts(summary)


if __name__ == "__main__":
    main()