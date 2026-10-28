# Transaction Data ETL Pipeline

A beginner data engineering project that demonstrates how to validate, transform, and load transaction data from CSV files into PostgreSQL using Python and SQL.

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline that processes transaction records, performs data quality checks, cleans the source data, and loads the results into a PostgreSQL database.

It also includes SQL analytics queries for summarizing transaction values, comparing transaction statuses, and classifying transactions by value.

## Architecture

```text
Raw CSV Data
    |
    v
Data Quality Checks
    |
    v
Extract and Transform (Python + pandas)
    |
    v
Processed CSV
    |
    v
Load to PostgreSQL (SQLAlchemy + psycopg)
    |
    v
SQL Analytics and Reports
```

## Technologies Used

- Python
- pandas
- PostgreSQL
- SQLAlchemy
- psycopg
- python-dotenv
- SQL

## Project Structure

```text
data-engineering-project/
├── data/
│   ├── raw/
│   │   └── transactions.csv
│   └── processed/
├── sql/
│   ├── create_tables.sql
│   └── analytics.sql
├── src/
│   ├── data_quality.py
│   ├── extract_transform.py
│   ├── load_to_postgres.py
│   └── run_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- Validates required columns and missing values.
- Detects duplicate transaction IDs.
- Checks numeric transaction amounts and invalid dates.
- Identifies negative amounts and unexpected transaction statuses.
- Transforms raw transaction data using pandas.
- Loads records into PostgreSQL using UPSERT logic.
- Includes SQL reports using aggregation, filtering, grouping, sorting, and conditional classification.
- Uses environment variables for database credentials.

## Prerequisites

- Python installed on your computer
- PostgreSQL
- Git
- A PostgreSQL database named `data_engineering`

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd data-engineering-project
```

Replace the placeholder with your actual repository URL.

### 2. Create a virtual environment

On Windows:

```powershell
py -m venv .venv
```

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_engineering
```

Replace the example password with your local PostgreSQL password. Never commit your `.env` file.

### 5. Create the database and table

Create the `data_engineering` database in PostgreSQL if it does not exist.

Execute `sql/create_tables.sql` against that database using pgAdmin or another PostgreSQL client.

### 6. Run the ETL pipeline

```powershell
.\.venv\Scripts\python.exe .\src\run_pipeline.py
```

### 7. Run the SQL analytics

Execute the queries in `sql/analytics.sql` using pgAdmin's Query Tool.

## Sample Data

The project uses transaction records with fields for transaction ID, date, customer ID, amount, currency, and status.

The included sample data is intended for learning and demonstration.

## Learning Outcomes

This project demonstrates practical experience with:

- Building a Python ETL pipeline
- Performing data quality checks
- Cleaning structured data
- Connecting Python to PostgreSQL
- Handling existing records through UPSERT
- Writing SQL analytics queries
- Managing local database configuration securely

## Future Improvements

- Add automated unit tests.
- Add structured logging and error handling.
- Introduce incremental data processing.
- Schedule pipeline execution.
- Add data quality reporting and monitoring.

## Disclaimer

This is an educational portfolio project using sample transaction data. It is not intended for processing production financial data without additional security, testing, monitoring, and operational controls.
