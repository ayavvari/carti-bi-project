# CARTI Business-Intelligence Projects

This repository contains two Python-based business intelligence projects inspired by the Director of Health Informatics position at CARTI. These projects demonstrate how a BI analyst can integrate clinical (SG2) data with CRM (Salesforce) and operational datasets to produce actionable insights, predictive models and reports.

## Project 1: Healthcare Business‑Intelligence Demo

This project shows how to integrate patient‑flow data (similar to SG2) with Salesforce CRM data, perform ETL, fit a regression model and expose results via a RESTful API.

### Structure

- `data_generation.py` – Generates synthetic patient‑flow data and Salesforce provider data and saves them as CSV files.
- `analysis.py` – Performs ETL: loads the CSV files, aggregates metrics, merges the datasets, computes ROI metrics and fits a linear regression model to predict deal values. It also saves a summary CSV.
- `api.py` – Provides a simple Flask API exposing aggregated metrics and detailed provider records from a SQLite database.
- `requirements.txt` – Lists the Python dependencies.

### Getting Started

1. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Generate the datasets**

    ```bash
    python data_generation.py
    ```
    This will create `sg2_patient_flow.csv` and `salesforce_providers.csv` in the project directory.

3. **Run the analysis**

    ```bash
    python analysis.py
    ```
    The script will produce a `provider_summary.csv` with aggregated metrics and regression predictions.

4. **Run the API**

    ```bash
    python api.py
    ```
    The Flask app exposes endpoints to retrieve provider summaries and details.

### Insights

This demo illustrates how to quantify ROI by linking referral volumes and satisfaction data to CRM deal values—a key skill for analyzing business development opportunities.

## Project 2: CARTI Informatics Project

This more advanced project expands on the demo by integrating three data sources—SG2 patient‑flow, Salesforce CRM and inventory usage—to mirror the complexity of CARTI’s statewide oncology operations and Nicholas Brady’s interests in health informatics and supply‑chain management.

### Structure

- `generate_informatics_data.py` – Generates synthetic SG2 patient‑flow data, Salesforce CRM provider data and inventory usage data. The patient‑flow dataset includes service lines, admission/discharge dates, lengths of stay, costs and satisfaction scores; the inventory dataset represents supplies consumed per patient.
- `etl_informatics_analysis.py` – Performs ETL and analysis: aggregates patient metrics (volume, length of stay, satisfaction, cost) by provider and service line, merges these with CRM metrics (contact count, pipeline stage, deal value) and inventory metrics (average supplies per patient) and calculates opportunity value per patient. It fits a linear regression model to predict opportunity value based on clinical and operational variables.
- **Output files** (created by running `etl_informatics_analysis.py`):
  - `provider_merged_summary_informatics.csv` – Merged provider‑level metrics including ROI and predicted opportunity.
  - `patient_volume_service_line_informatics.png` – Bar chart visualizing patient volume by service line.
  - `opportunity_vs_cost_informatics.png` – Scatter plot comparing average treatment cost to total opportunity value by provider.
  - `predicted_vs_actual_informatics.png` – Plot comparing predicted vs. actual opportunity values to evaluate model performance.
- `README_INFORMATICS.md` – Stand‑alone description of the project and step‑by‑step instructions.

### Running the Project

1. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Generate data & run analysis**

    ```bash
    python generate_informatics_data.py
    python etl_informatics_analysis.py
    ```

    This will create the merged summary CSV and plots in the repository.

### Insights & Applicability

- **Data integration** – Demonstrates ETL and data‑warehousing skills by unifying clinical, CRM and inventory datasets, addressing common interoperability challenges.
- **Predictive analytics** – Uses regression modeling to forecast opportunity value from patient volume, satisfaction, costs and supply usage, showcasing statistical‑modeling experience.
- **Operational intelligence** – Combines financial and operational metrics to highlight high‑value service lines and providers, supporting strategic decisions such as outreach, staffing and supply planning.
- **Alignment with CARTI’s mission** – Reflects Nicholas Brady’s focus on health informatics, strategic sourcing and patient outcomes, illustrating how BI tools can drive cancer‑care innovation.

---

These projects can serve as a template for real‑world BI initiatives at CARTI, demonstrating proficiency in SQL/ETL, data visualization, statistical modeling and report generation—skills emphasized in the job description.