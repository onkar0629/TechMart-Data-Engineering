
# TechMart Data Engineering

TechMart is a production-style e-commerce data engineering portfolio project designed for SQL, Python, Azure, PySpark, data warehousing, and Power BI workflows.

## Objectives

- Model a realistic e-commerce platform similar to Amazon, Flipkart, or Walmart.
- Generate large-scale synthetic transactional data.
- Provide a modular, scalable foundation for analytics and cloud integrations.
- Support future growth from development datasets to enterprise-scale workloads.

## Repository Structure

- database/ - MySQL schema and database objects
- generator/ - modular synthetic data generation framework
- generator/output/ - generated CSV datasets

## Tech Stack

- MySQL
- Python 3
- pandas, numpy, Faker
- PySpark
- Azure Data Factory / Azure SQL / Azure Blob Storage
- Power BI

## Getting Started

1. Install dependencies:
   pip install -r requirements.txt
2. Create the MySQL schema:
   mysql < database/schema.sql
3. Generate synthetic datasets:
   python3 -m generator.main

## Scaling the generator

Update values in generator/config.py to increase or decrease data volume.

## Output

Generated CSV files are written to generator/output/.

## Roadmap

- Phase 1: transactional schema and dataset generation
- Phase 2: SQL analytics and data quality checks
- Phase 3: Azure ingestion and warehousing
- Phase 4: Power BI dashboarding and reporting
