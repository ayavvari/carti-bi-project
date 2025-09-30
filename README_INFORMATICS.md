# CARTI Informatics BI Project

This project is a proof‑of‑concept designed to mirror the responsibilities
outlined in a health‑informatics role at CARTI.  It integrates data from
simulated sources—SG2 patient flow, Salesforce CRM and supply‑chain inventory—to
produce insights that could inform business development, operational planning
and provider engagement.

## Objectives

* **Subject‑matter expertise in Salesforce and SG2:** Generate and merge
  synthetic SG2 data with simplified Salesforce CRM records to analyze provider
  performance and identify opportunities for growth.
* **Technical project management:** Demonstrate an end‑to‑end workflow that
  includes requirements (data generation), ETL (merging datasets), analysis,
  visualization and simple predictive modeling.
* **ROI and operational metrics:** Compute revenue and cost proxies (e.g.,
  opportunity value, treatment cost) and relate them to patient volume and
  satisfaction.  Provide summary tables and dashboards.
* **Data warehousing & ETL:** Store data in CSVs that could easily be loaded
  into a database or data warehouse.  The `etl_analysis.py` script handles
  extraction, transformation and loading into a unified DataFrame.
* **Supply chain insight:** Incorporate inventory usage to reflect Nicholas
  Brady’s background in strategic sourcing and pharmacy operations; show how
  clinical volume impacts inventory needs.

## Project Structure

| File | Description |
|---|---|
| **`generate_data.py`** | Creates synthetic SG2 patient flow data, Salesforce CRM data and inventory usage data, saving them as CSV files. |
| **`etl_analysis.py`** | Performs ETL on the generated datasets, merges them by provider, computes metrics, trains a linear regression model and outputs summary tables and charts. |
| **`sg2_patient_flow.csv`** | Synthetic patient flow data; includes admission/discharge dates, service line, satisfaction and cost. |
| **`salesforce_crm.csv`** | Simplified CRM records of referring providers with pipeline stages and opportunity value. |
| **`inventory_usage.csv`** | Supply‑chain data showing inventory levels and usage per provider and item. |
| **`provider_merged_summary.csv`** | Resulting summary table after ETL and analysis. |
| **`patient_volume_service_line.png`** | Bar chart of patient volumes by service line. |
| **`opportunity_vs_cost.png`** | Scatter plot of opportunity value vs. average treatment cost per provider. |
| **`predicted_vs_actual.png`** | Visualization comparing predicted and actual opportunity values from the regression model. |

## Running the Project

1. **Generate Data** – Navigate to the project directory and run:

   ```bash
   python generate_data.py
   ```

   This will create `sg2_patient_flow.csv`, `salesforce_crm.csv` and
   `inventory_usage.csv` in the current directory.

2. **Perform ETL and Analysis** – Run:

   ```bash
   python etl_analysis.py
   ```

   This script reads the generated datasets, merges them, computes summary
   metrics by provider, trains a regression model and saves the outputs.

## Interpretation & Alignment

### Business Development & ROI

The merged dataset allows you to compare provider engagement (contacts and
pipeline stage) with clinical activity (patient volume, satisfaction, cost).  A
BI analyst can use this information to prioritize outreach, refine referral
strategies and quantify potential return on investment.

### Operational Efficiency & Supply Chain

By integrating inventory usage, the project demonstrates how clinical volumes
impact supply needs.  This aligns with Nicholas Brady’s experience in supply
chain management and pharmacy operations.  The data can inform reorder
strategies and identify providers whose usage patterns deviate from norms.

### Predictive Modeling & Advanced Analytics

The simple linear regression model predicts opportunity value based on clinical
and operational features.  This shows familiarity with statistical modeling and
data science tools (Python) and can be extended to more sophisticated models or
implemented in other languages like R or STATA.

### Reporting & Visualization

Visualizations and the summary table can be used to build dashboards in Power BI
or Tableau, satisfying the requirement for automated reporting tools and
professional presentation of insights.  The project structure also lends itself
to agile development practices and could be deployed via RESTful APIs.