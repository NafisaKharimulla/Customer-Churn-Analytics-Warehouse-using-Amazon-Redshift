# Serverless Student Performance Analytics System

## Overview

This project demonstrates a **serverless data analytics system** using **Amazon Redshift Serverless**, **S3**, **Python**, and **SQL**.  
It processes student and telecom datasets, performs ETL (Extract, Transform, Load), and generates analytical insights without managing traditional database clusters.

## Project Structure

```
/Serverless-Student-Performance-Analytics
│
├─ /documents         # Task documents and explanations
├─ /screenshots       # Screenshots of results and queries
├─ /scripts           # Python scripts and SQL scripts
│   ├─ load.py
│   ├─ analytics.py
│   └─ task_queries.sql
├─ README.md          # Project overview and instructions
└─ requirements.txt   # Python dependencies
```

## Dataset

- `telecom_customer_churn.csv` – Contains telecom customer churn data.
- `telecom_zipcode_population.csv` – Contains population data by zip code.

**Columns in customer churn CSV:**

- `customer_id`, `gender`, `age`, `married`, `num_dependents`, `city`, `zip_code`, `latitude`, `longitude`, `num_referrals`

**Columns in zip population CSV:**

- `zipcode`, `population`

## Tasks Completed

1. **Create Workgroup and Namespace**
   - Setup Amazon Redshift Serverless workgroup and namespace.
   - Configured IAM role for S3 access.

2. **Create Database Tables**
   - Created staging tables in Redshift matching CSV datasets.

3. **Load Data into Redshift**
   - Used **COPY** command to load CSV data from S3.
   - Handled headers, delimiters, and NULL values.

4. **Create Analytical Table**
   - Joined customer churn and population tables.
   - Selected relevant columns: `customer_id`, `city`, `zip_code`, `population`, etc.
   - Applied DISTKEY and SORTKEY for optimization.

5. **Data Analysis**
   - Queries for churn rate, top cities by churn, tenure distribution, lost revenue, and population vs. customer count.
   - Scripts saved in `task_queries.sql` and `analytics.py`.

6. **Redshift Optimization**
   - Performed `ANALYZE` to update table statistics.
   - Performed `VACUUM` to reorganize storage and improve query performance.

7. **Clean Up Resources**
   - Deleted workgroup and namespace.
   - Removed S3 objects and temporary data.
   - Removed IAM roles used for project.

## Python Scripts

- `load.py` – Loads data from CSV files to Redshift Serverless.
- `analytics.py` – Executes analytical queries using Redshift Data API.
- Other utility scripts for S3 operations and data processing.

## Requirements

- Python 3.10+
- Packages: `boto3`, `pandas`, `psycopg2-binary`
- AWS account with S3 and Redshift Serverless access

Install dependencies:

```bash
pip install -r requirements.txt

Author
Nafisa Shaik
```
