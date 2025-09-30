"""
Generate synthetic patient‑flow and Salesforce provider datasets.

This script creates two CSV files:
  - `sg2_patient_flow.csv` containing simulated patient encounters across various service lines.
  - `salesforce_providers.csv` containing simulated Salesforce CRM data for referring providers.

The random seed is fixed to produce reproducible results.
"""

import numpy as np
import pandas as pd


def generate_patient_flow(num_patients: int = 1000) -> pd.DataFrame:
    """Create a synthetic SG2-like patient flow dataset."""
    np.random.seed(42)
    providers = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Jones']
    service_lines = ['Surgery', 'Behavioral Health', 'Orthopedics', 'Cardiology', 'Oncology']
    
    df = pd.DataFrame({
        'patient_id': range(1, num_patients + 1),
        'referral_provider': np.random.choice(providers, num_patients),
        'service_line': np.random.choice(service_lines, num_patients),
        'admission_date': pd.to_datetime('2025-01-01') + pd.to_timedelta(
            np.random.randint(0, 365, num_patients), unit='D'
        )
    })
    df['length_of_stay'] = np.random.randint(1, 11, num_patients)
    df['discharge_date'] = df['admission_date'] + pd.to_timedelta(df['length_of_stay'], unit='D')
    df['satisfaction_score'] = np.random.normal(loc=80, scale=10, size=num_patients).clip(0, 100)
    return df


def generate_salesforce_data(providers: list) -> pd.DataFrame:
    """Create a synthetic Salesforce provider dataset."""
    stages = ['Prospecting', 'Qualified', 'Proposal', 'Closed Won', 'Closed Lost']
    np.random.seed(24)
    data = {
        'account_id': range(1, len(providers) + 1),
        'provider_name': providers,
        'pipeline_stage': np.random.choice(stages, len(providers)),
        'contact_count': np.random.randint(5, 50, len(providers)),
        'deals_value': np.random.randint(50_000, 500_000, len(providers))
    }
    return pd.DataFrame(data)


if __name__ == '__main__':
    # Generate and save the datasets
    patient_flow_df = generate_patient_flow()
    patient_flow_df.to_csv('sg2_patient_flow.csv', index=False)

    providers_list = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Jones']
    salesforce_df = generate_salesforce_data(providers_list)
    salesforce_df.to_csv('salesforce_providers.csv', index=False)
    
    print('Datasets generated: sg2_patient_flow.csv and salesforce_providers.csv')