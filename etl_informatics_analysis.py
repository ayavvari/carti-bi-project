"""
ETL and Analysis for CARTI Informatics Project
---------------------------------------------

This script performs a mock ETL (Extract, Transform, Load) process that
integrates SG2 patient flow data, Salesforce CRM data and inventory usage data.
It computes summary metrics, merges datasets on the referring provider and
analyzes relationships between patient volumes, satisfaction, treatment cost,
opportunity value and inventory usage.  The script also trains a linear
regression model to illustrate how a BI analyst might predict potential
opportunity value based on clinical and operational variables.

Outputs include summary CSVs and visualizations saved to the project directory.

Usage::

    python etl_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sg2 = pd.read_csv('sg2_patient_flow.csv', parse_dates=['admission_date', 'discharge_date'])
    crm = pd.read_csv('salesforce_crm.csv')
    inventory = pd.read_csv('inventory_usage.csv', parse_dates=['date'])
    return sg2, crm, inventory

def transform_and_merge(sg2: pd.DataFrame, crm: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregate metrics per provider and merge datasets."""
    # Aggregate patient flow metrics by provider
    agg = sg2.groupby('referring_provider').agg(
        total_patients=('patient_id', 'count'),
        avg_length_of_stay=('length_of_stay', 'mean'),
        avg_satisfaction=('satisfaction_score', 'mean'),
        avg_cost=('treatment_cost', 'mean')
    ).reset_index().rename(columns={'referring_provider': 'provider_name'})
    # Aggregate inventory metrics per provider
    inv_agg = inventory.groupby('provider_name').agg(
        total_quantity_on_hand=('quantity_on_hand', 'sum'),
        avg_daily_usage=('daily_usage', 'mean'),
        total_items=('item_name', 'count')
    ).reset_index()
    # Merge with CRM
    merged = agg.merge(crm, on='provider_name', how='left').merge(inv_agg, on='provider_name', how='left')
    return merged

def train_regression(df: pd.DataFrame) -> tuple[LinearRegression, pd.DataFrame]:
    """Train a regression model to predict opportunity value."""
    # Prepare features and target
    features = df[['total_patients', 'avg_length_of_stay', 'avg_satisfaction', 'avg_cost', 'total_quantity_on_hand', 'avg_daily_usage']]
    # Replace NaN with zeros (inventory may be missing for some providers)
    features = features.fillna(0)
    target = df['opportunity_value']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    print(f'Linear regression R^2 on test set: {r2:.2f}')
    # Add predictions to DataFrame
    df['predicted_opportunity_value'] = model.predict(features)
    return model, df

def save_outputs(df: pd.DataFrame) -> None:
    """Save summary CSV and create visualizations."""
    df.to_csv('provider_merged_summary.csv', index=False)
    # Plot patient volume by service line
    # This requires original sg2 dataset; we load inside this function
    sg2 = pd.read_csv('sg2_patient_flow.csv')
    service_counts = sg2['service_line'].value_counts().sort_values()
    plt.figure(figsize=(8, 4))
    service_counts.plot(kind='barh', color='steelblue')
    plt.title('Patient Volume by Service Line')
    plt.xlabel('Number of Patients')
    plt.ylabel('Service Line')
    plt.tight_layout()
    plt.savefig('patient_volume_service_line.png')
    plt.close()
    # Plot opportunity value vs. average cost per provider
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x='avg_cost', y='opportunity_value', data=df, hue='provider_name', s=60)
    plt.title('Opportunity Value vs. Average Treatment Cost')
    plt.xlabel('Average Treatment Cost')
    plt.ylabel('Opportunity Value')
    plt.tight_layout()
    plt.savefig('opportunity_vs_cost.png')
    plt.close()
    # Plot predicted vs. actual opportunity value
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x='opportunity_value', y='predicted_opportunity_value', data=df, hue='provider_name', s=60)
    plt.plot([df['opportunity_value'].min(), df['opportunity_value'].max()],
             [df['opportunity_value'].min(), df['opportunity_value'].max()], 'k--', lw=1)
    plt.title('Predicted vs. Actual Opportunity Value')
    plt.xlabel('Actual Opportunity Value')
    plt.ylabel('Predicted Opportunity Value')
    plt.tight_layout()
    plt.savefig('predicted_vs_actual.png')
    plt.close()

def main() -> None:
    sg2, crm, inventory = load_datasets()
    merged_df = transform_and_merge(sg2, crm, inventory)
    model, enriched_df = train_regression(merged_df)
    save_outputs(enriched_df)
    print('ETL and analysis complete. Outputs saved.')

if __name__ == '__main__':
    main()