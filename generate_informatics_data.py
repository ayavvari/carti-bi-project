"""
Data Generation for CARTI Informatics Project
-------------------------------------------

This module produces three synthetic datasets to support a proof‑of‑concept
business‑intelligence project for CARTI.  The goal is to emulate common data
sources that a health informatics team might integrate when seeking
opportunities across patient flow (SG2), CRM interactions (Salesforce), and
supply‑chain operations.

Datasets:

1. **sg2_patient_flow.csv** – Represents de‑identified patient encounters with
   service lines, admission/discharge dates, satisfaction scores, costs and
   referring providers.  This simulates SG2 output used to analyze patient
   volume, care pathways and outcomes.
2. **salesforce_crm.csv** – Contains simplified CRM records of referring
   providers.  Fields include pipeline stage, number of contacts and potential
   opportunity value.  Linking this to patient flow reveals which providers
   generate high value referrals.
3. **inventory_usage.csv** – Models supply‑chain and pharmacy data at the
   provider level.  It tracks quantities of key items, their usage rates and
   reorder points.  This helps illustrate how clinical volumes drive
   inventory needs.

Running this module writes the CSV files to the project directory.

Usage::

    python generate_data.py
"""

import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Reference lists
PROVIDERS = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Jones']
SERVICE_LINES = [
    'Surgical Oncology', 'Medical Oncology', 'Radiation Oncology',
    'Diagnostic Imaging', 'Urology', 'Breast Center'
]
PIPLINE_STAGES = ['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
ITEMS = ['Chemo Drug A', 'Chemo Drug B', 'Radiation Supplies', 'Surgical Kit', 'Imaging Contrast']

def generate_sg2_data(num_patients: int = 1000) -> pd.DataFrame:
    """Create synthetic SG2 patient flow data."""
    data = []
    for pid in range(1, num_patients + 1):
        provider = np.random.choice(PROVIDERS)
        service_line = np.random.choice(SERVICE_LINES)
        admission = pd.to_datetime('2025-01-01') + pd.to_timedelta(
            np.random.randint(0, 365), unit='D'
        )
        length_of_stay = np.random.randint(1, 10)
        discharge = admission + pd.to_timedelta(length_of_stay, unit='D')
        satisfaction = np.random.normal(loc=85, scale=8)
        satisfaction = np.clip(satisfaction, 50, 100)
        cost = np.random.normal(loc=5000, scale=1500)
        cost = max(1000, cost)  # ensure positive
        payer = np.random.choice(['Medicare', 'Medicaid', 'Commercial', 'Self‑Pay'])
        data.append({
            'patient_id': pid,
            'referring_provider': provider,
            'service_line': service_line,
            'admission_date': admission.strftime('%Y-%m-%d'),
            'discharge_date': discharge.strftime('%Y-%m-%d'),
            'length_of_stay': length_of_stay,
            'satisfaction_score': round(float(satisfaction), 2),
            'treatment_cost': round(float(cost), 2),
            'payer': payer
        })
    return pd.DataFrame(data)

def generate_salesforce_data() -> pd.DataFrame:
    """Create synthetic Salesforce CRM data for providers."""
    data = []
    for provider in PROVIDERS:
        stage = np.random.choice(PIPLINE_STAGES, p=[0.25, 0.25, 0.2, 0.15, 0.1, 0.05])
        contacts = np.random.randint(5, 50)
        opportunity_value = np.random.randint(50_000, 500_000)
        data.append({
            'provider_name': provider,
            'pipeline_stage': stage,
            'contact_count': contacts,
            'opportunity_value': opportunity_value
        })
    return pd.DataFrame(data)

def generate_inventory_data() -> pd.DataFrame:
    """Create synthetic inventory usage data per provider and item."""
    data = []
    for provider in PROVIDERS:
        for item in ITEMS:
            quantity_on_hand = np.random.randint(10, 100)
            daily_usage = np.random.randint(1, 10)
            reorder_point = np.random.randint(5, 20)
            date = pd.to_datetime('2025-01-01') + pd.to_timedelta(
                np.random.randint(0, 30), unit='D'
            )
            data.append({
                'provider_name': provider,
                'item_name': item,
                'date': date.strftime('%Y-%m-%d'),
                'quantity_on_hand': quantity_on_hand,
                'daily_usage': daily_usage,
                'reorder_point': reorder_point
            })
    return pd.DataFrame(data)

def main() -> None:
    sg2_df = generate_sg2_data()
    crm_df = generate_salesforce_data()
    inventory_df = generate_inventory_data()
    sg2_df.to_csv('sg2_patient_flow.csv', index=False)
    crm_df.to_csv('salesforce_crm.csv', index=False)
    inventory_df.to_csv('inventory_usage.csv', index=False)
    print('Generated sg2_patient_flow.csv, salesforce_crm.csv and inventory_usage.csv')

if __name__ == '__main__':
    main()