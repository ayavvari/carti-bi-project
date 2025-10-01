# CARTI Healthcare BI Project

This repository contains an end‑to‑end healthcare business intelligence solution built to
demonstrate data engineering, predictive modelling, RESTful API development and
interactive reporting skills in the context of CARTI’s mission.  The project
integrates data from synthetic versions of SG2 patient flow analytics, Salesforce
CRM and electronic health records (EHR) to provide actionable insights on
patient trends, provider performance and return on investment (ROI).

## Project Components

1. **Data Generation (`generate_full_data.py`)** –
   Creates synthetic datasets to simulate SG2 patient flow, Salesforce CRM
   metrics and EHR clinical/claims data.  The generated CSV files are:

   - `sg2_patient_flow_full.csv` – patient demographics, service lines,
     admission/discharge dates, satisfaction scores and treatment costs.
   - `salesforce_crm_full.csv` – provider CRM metrics (contact counts,
     opportunity values, marketing costs, pipeline stages).
   - `ehr_data_full.csv` – visit‑level clinical and financial information
     (diagnosis codes, procedure codes, claim amounts/paid status) for each
     patient.

2. **ETL & Analytics (`etl_full_analysis.py`)** –
   Loads the three raw datasets, cleans and integrates them into a unified
   provider‑level summary.  Key tasks include:
   - Aggregating patient flow data by provider (count, average length of stay,
     satisfaction and cost).
   - Summarising EHR claims by provider (total visits, total claim amounts,
     claim collection rate and denial rate).
   - Merging CRM metrics with clinical and financial data.
   - Calculating ROI and value per patient.
   - Training a linear regression model to predict opportunity value based on
     provider metrics; predicted values are added to the summary.
   - Exporting outputs:
     * `provider_summary_full.csv` – provider metrics with actual and predicted
       opportunity values.
     * `carti_full_powerbi_dataset.xlsx` – multi‑sheet workbook containing
       SG2, CRM, EHR and summary tables for import into Power BI.
     * `roi_by_provider.png` and `predicted_vs_actual_opportunity.png` –
       illustrative charts of ROI and model performance.

3. **Web API (`api/`)** –
   A minimal ASP.NET 6 Web API providing RESTful endpoints to access the
   provider summary and model results.  Endpoints include:
   - `GET /providers` – returns all provider summary records.
   - `GET /providers/{name}` – returns metrics for a specific provider.
   - `GET /predictions/opportunity?provider=Name` – returns the predicted
     opportunity value for a provider.
   The API reads data from `provider_summary_full.csv` on startup.  In a
   production setting this would be replaced with a proper database or
   caching layer.

4. **Power BI Demo (`carti_full_powerbi_dataset.xlsx`)** –
   An Excel workbook with four sheets (SG2, CRM, EHR and summary) ready to
   import into Power BI.  Suggested visuals:
   - Patient volume trends by service line and provider.
   - Provider performance (volume, satisfaction, claim metrics).
   - ROI analysis comparing deals value, marketing cost and calculated ROI.
   - Predicted vs. actual opportunity value scatter plot.
   Use slicers for service line, provider or timeframe to enable interactive
   exploration of the data.

5. **DevOps & Agile Considerations** –
   Although this repository contains static scripts, the code has been
   structured to support continuous integration and deployment.  Suggested
   enhancements include:
   - Setting up a CI pipeline (e.g., GitHub Actions or Azure Pipelines) to run
     `generate_full_data.py` and `etl_full_analysis.py`, run unit tests and
     build the ASP.NET API.
   - Packaging the API into a Docker container or Azure App Service for
     deployment.
   - Creating a deployment pipeline for the Power BI report using Power BI
     deployment pipelines.
   - Tracking requirements and work items using a Scrum board in Azure
     DevOps or Jira.

## How to Run

1. Clone this repository and install Python dependencies (e.g., using
   `pip install pandas numpy scikit-learn matplotlib xlsxwriter`).
2. Execute `python generate_full_data.py` to generate the raw CSV files.
3. Run `python etl_full_analysis.py` to build the provider summary, train
   the predictive model and export the outputs.
4. (Optional) Build and run the Web API:
   ```bash
   cd api
   dotnet restore
   dotnet run
   ```
   The API will be accessible at `http://localhost:5000`.  See
   `Program.cs` for available endpoints.
5. Open `carti_full_powerbi_dataset.xlsx` in Power BI Desktop and create
   reports/dashboards using the suggestions above.

## License

This project is provided for educational and demonstration purposes and
includes synthetic data.  No real patient data is included.