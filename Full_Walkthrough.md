# End‑to‑End Healthcare BI Project Walkthrough

## Overview

This document provides a narrative walkthrough of the CARTI healthcare
business intelligence project contained in this repository.  The goal of
the project is to showcase how disparate healthcare data sources can be
integrated, analysed and presented in a meaningful way to support
decision‑makers.  While the data included here is synthetic, the
architecture and techniques mirror what would be required in a real
deployment.

## Business Context

CARTI’s mission is to make trusted cancer care accessible to every
patient and to be Arkansas’ cancer treatment destination【40511613335181†L96-L105】.  To
achieve this mission, leadership needs timely insights into how
patients enter and move through the network (referral patterns), how
providers are performing (volume, quality and financial impact) and
where marketing and outreach dollars are generating the best return.
Traditional reporting suffers from fragmented systems, manual data
collection and limited forward‑looking analytics【186091743127646†L418-L474】.  This
project demonstrates an integrated solution that addresses those
challenges.

## Data Sources

The solution unifies three categories of data:

1. **SG2 Patient Flow Analytics** – Aggregate market and patient flow
   data, indicating where patients originate and how they move through
   service lines.  In the synthetic dataset, this includes patient
   demographics, service lines, admission/discharge dates, satisfaction
   scores and treatment costs.
2. **Salesforce CRM** – Referral and marketing data such as contact
   counts, pipeline stages, opportunity values, deals values and
   marketing spend.  Linking CRM data to clinical outcomes enables
   measurement of marketing ROI.
3. **Electronic Health Records (EHR)** – Visit‑level clinical and
   financial records including diagnoses, procedures, claim amounts and
   claim payment status.  EHR data provides the ground truth for
   clinical workload and revenue.

## Technical Architecture

The architecture follows a modular pattern:

1. **Data generation** – A Python script (`generate_full_data.py`)
   produces synthetic data for SG2, CRM and EHR.  In a live system, this
   would be replaced with automated extraction from SG2 files,
   Salesforce APIs and the EHR database.
2. **ETL** – The ETL script (`etl_full_analysis.py`) reads the raw
   datasets, transforms them and loads them into an integrated
   provider‑level summary.  Key metrics are calculated, including ROI,
   value per patient and claim collection rates.  The script also
   trains a regression model to predict opportunity value, adding the
   predictions back to the summary.
3. **Data warehouse and reporting** – For demonstration, the ETL
   exports a multi‑sheet Excel file (`carti_full_powerbi_dataset.xlsx`),
   which can be loaded into Power BI.  In production, the integrated
   tables would be stored in a SQL database (e.g., SQL Server or
   Synapse) and queried directly by reporting tools.
4. **Predictive analytics** – A simple linear regression model is
   trained to predict opportunity values based on provider metrics.
   This illustrates how predictive models can augment descriptive
   reports by forecasting future revenue potential【12†L138-L146】.
5. **RESTful API** – A minimal ASP.NET Core Web API exposes provider
   summary metrics and prediction results.  This demonstrates how
   analytics can be consumed programmatically by other applications,
   such as portals, EHR systems or mobile apps.  It also shows
   proficiency in C# and modern API design.
6. **Dashboarding** – The Power BI dataset enables construction of
   interactive dashboards.  Suggested visuals include patient volume
   trends, provider rankings and ROI comparisons.  When users filter
   one visual, all other visuals cross‑filter automatically, revealing
   insights across multiple dimensions【4†L259-L267】.

## Execution Instructions

To reproduce this project locally:

1. **Install dependencies** – Install Python packages (pandas, numpy,
   scikit‑learn, matplotlib, xlsxwriter) and .NET 6 SDK if you wish to
   run the API.
2. **Generate data** – Execute `python generate_full_data.py` in the
   `carti_full_project` directory.  This will create three CSV files
   containing synthetic SG2, CRM and EHR data.
3. **Run ETL and analytics** – Run `python etl_full_analysis.py` to
   transform the raw data, compute metrics, train the predictive model
   and export the provider summary, charts and Power BI workbook.  The
   script prints model evaluation metrics (MAE and R²) to the console
   and saves the files `provider_summary_full.csv`,
   `roi_by_provider.png`, `predicted_vs_actual_opportunity.png` and
   `carti_full_powerbi_dataset.xlsx`.
4. **Use the API** – Navigate to the `api` folder, restore NuGet
   packages (`dotnet restore`) and run (`dotnet run`).  The API will
   start locally and serve endpoints for provider summaries and
   predictions.
5. **Build dashboards** – Open the Excel workbook in Power BI Desktop.
   Create visuals such as bar charts, line charts and KPIs to monitor
   patient volumes, provider performance and ROI.  Use slicers to
   explore data by service line, provider or time.

## Limitations & Future Work

- The datasets are synthetic and simplified; real SG2, CRM and EHR data
  would contain more complexity and nuance.  Further enhancements
  could incorporate additional tables (e.g., medication data,
  appointment no‑show flags) and more sophisticated feature engineering.
- The predictive model is a basic linear regression.  More advanced
  models (e.g., gradient boosting, time series models) could improve
  forecasting accuracy.  Additionally, classification models could be
  added to predict outcomes like readmissions or claim denials.
- The API loads data from a CSV file at startup.  A robust system
  would use a relational database or data lake with change tracking.
- The project does not include user authentication or row‑level
  security in the dashboard.  These are essential in a production
  healthcare environment.

## Conclusion

This end‑to‑end project demonstrates the core competencies of a
healthcare data engineer and analyst: integrating heterogeneous data,
building ETL pipelines, applying predictive modelling, creating
RESTful services and producing intuitive dashboards.  By following
these patterns with real data at CARTI, a health‑informatics team can
provide actionable insights that support strategic growth, improve
patient outcomes and maximise return on investment【7†L236-L244】.