"""Generate synthetic healthcare data for CARTI end‑to‑end BI project.

This script produces three CSV files representing data from SG2 patient
flow analytics, Salesforce CRM, and an electronic health record (EHR)
system. The goal is to simulate a realistic mix of operational,
clinical and business data that can be ingested into the BI solution.

Generated files:
  - sg2_patient_flow_full.csv: Synthetic patient flow and forecasting data.
  - salesforce_crm_full.csv: Synthetic CRM metrics for referring providers.
  - ehr_data_full.csv: Synthetic EHR clinical and financial records.

The data sets are deliberately simple yet rich enough to support
demonstrations of ETL, predictive modelling and dashboard reporting.
"""

import numpy as np
import pandas as pd


def generate_data(num_patients: int = 2000, num_providers: int = 8) -> None:
    """Generate synthetic SG2, CRM and EHR data and save as CSV files.

    Args:
        num_patients: Number of unique patients to generate.
        num_providers: Number of unique referring providers (physicians).

    The synthetic patient population includes demographic attributes,
    random service lines, admission/discharge dates, satisfaction scores
    and costs. Providers each have their own CRM metrics such as
    opportunities and marketing spend. The EHR records contain visits,
    diagnoses, procedures and claims information for each patient.
    """
    rng = np.random.default_rng(42)

    # Define lists of providers and service lines
    provider_names = [
        f"Dr. {last_name}" for last_name in [
            "Smith", "Johnson", "Williams", "Brown",
            "Jones", "Garcia", "Miller", "Davis"]
    ][:num_providers]

    service_lines = [
        "Oncology", "Cardiology", "Orthopedics",
        "Surgery", "Behavioral Health", "Urology"
    ]

    # Generate SG2 patient flow data
    patient_ids = np.arange(1, num_patients + 1)
    referral_providers = rng.choice(provider_names, size=num_patients)
    service_line_selection = rng.choice(service_lines, size=num_patients)

    # Generate random admission dates in the past year and length of stay
    base_date = pd.Timestamp("2025-01-01")
    admission_offsets = rng.integers(0, 365, size=num_patients)
    admission_dates = base_date + pd.to_timedelta(admission_offsets, unit="D")
    lengths_of_stay = rng.integers(1, 15, size=num_patients)
    discharge_dates = admission_dates + pd.to_timedelta(lengths_of_stay, unit="D")

    satisfaction_scores = rng.normal(loc=80, scale=10, size=num_patients).clip(50, 100)
    # Random cost of treatment per patient (simulate differences across service lines)
    base_costs = {
        "Oncology": 25000,
        "Cardiology": 18000,
        "Orthopedics": 22000,
        "Surgery": 30000,
        "Behavioral Health": 12000,
        "Urology": 15000,
    }
    costs = [
        base_costs[line] * rng.uniform(0.8, 1.2)
        for line in service_line_selection
    ]

    sg2_df = pd.DataFrame({
        "patient_id": patient_ids,
        "referral_provider": referral_providers,
        "service_line": service_line_selection,
        "admission_date": admission_dates,
        "length_of_stay": lengths_of_stay,
        "discharge_date": discharge_dates,
        "satisfaction_score": satisfaction_scores,
        "treatment_cost": costs,
    })

    # Generate CRM data for providers
    pipeline_stages = [
        "Prospecting", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"
    ]

    crm_records = []
    for provider in provider_names:
        contact_count = int(rng.integers(10, 80))
        deals_value = rng.integers(100_000, 600_000)
        opportunity_value = rng.integers(50_000, 400_000)
        marketing_cost = rng.integers(10_000, 60_000)
        stage = rng.choice(pipeline_stages)
        crm_records.append({
            "provider_name": provider,
            "contact_count": contact_count,
            "deals_value": deals_value,
            "opportunity_value": opportunity_value,
            "marketing_cost": marketing_cost,
            "pipeline_stage": stage,
        })
    crm_df = pd.DataFrame(crm_records)

    # Generate EHR clinical and financial records
    diagnoses = ["I10", "E11", "M16", "C50", "J45", "K35"]  # ICD-10 codes (hypertension, diabetes, etc.)
    procedures = ["99213", "93000", "27130", "47562", "99214", "52240"]  # CPT codes
    claim_statuses = ["Paid", "Denied", "Pending"]

    ehr_records = []
    for pid in patient_ids:
        # Each patient can have multiple visits (1-3)
        num_visits = rng.integers(1, 4)
        # Generate visits spread over the last year
        visit_dates = base_date + pd.to_timedelta(rng.integers(0, 365, size=num_visits), unit="D")
        for date in visit_dates:
            dx = rng.choice(diagnoses)
            proc = rng.choice(procedures)
            claim_amt = rng.uniform(5_000, 30_000)
            paid_ratio = rng.uniform(0.6, 1.0)
            claim_paid = claim_amt * paid_ratio
            status = rng.choice(claim_statuses, p=[0.8, 0.1, 0.1])
            provider = rng.choice(provider_names)
            ehr_records.append({
                "patient_id": pid,
                "visit_date": date,
                "diagnosis_code": dx,
                "procedure_code": proc,
                "provider_name": provider,
                "claim_amount": claim_amt,
                "claim_paid": claim_paid,
                "claim_status": status,
            })
    ehr_df = pd.DataFrame(ehr_records)

    # Save to CSV files
    sg2_df.to_csv("sg2_patient_flow_full.csv", index=False)
    crm_df.to_csv("salesforce_crm_full.csv", index=False)
    ehr_df.to_csv("ehr_data_full.csv", index=False)

    print("Synthetic data generated: sg2_patient_flow_full.csv, salesforce_crm_full.csv, ehr_data_full.csv")


if __name__ == "__main__":
    generate_data()