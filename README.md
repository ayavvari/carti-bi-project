# Healthcare Business‑Intelligence Project

This repository contains a Python implementation of a healthcare business‑intelligence project inspired by the CARTI role description.  The project demonstrates how to integrate patient‑flow data (similar to SG2) with Salesforce CRM data, perform ETL, build statistical models, and expose results via a RESTful API.

## Structure

- `data_generation.py` – Generates synthetic patient‑flow data and Salesforce provider data and saves them as CSV files.
- `analysis.py` – Performs ETL: loads the CSV files, aggregates metrics, merges the datasets, computes ROI metrics, and fits a linear regression model to predict deal values.  It also saves a summary CSV.
- `api.py` – Provides a simple Flask API exposing aggregated metrics and detailed provider records from a SQLite database.
- `requirements.txt` – Lists the Python dependencies.

## Getting Started

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

4. **Start the API**

   ```bash
   python api.py
   ```

   The API will listen on `http://localhost:5000` and expose endpoints such as `/providers` and `/providers/<name>`.

## Notes

- The data used here is synthetic and for demonstration purposes only.
- In a production environment, the ETL pipeline would be orchestrated with tools like Azure Data Factory or SSIS, and the API could be implemented in ASP.NET Core or another enterprise framework.
