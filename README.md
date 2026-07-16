
# TechMart Data Engineering

TechMart is a production-style e-commerce data engineering portfolio project designed for SQL, Python, Azure, PySpark, data warehousing, and Power BI workflows.

## Objectives

- Model a realistic e-commerce platform similar to Amazon, Flipkart, or Walmart.
- Generate large-scale synthetic transactional data.
- Provide a modular, scalable foundation for analytics and cloud integrations.
- Support future growth from development datasets to enterprise-scale workloads.

## Repository Structure

- docs/ - architecture, requirements, and dictionary documents
- database/ - MySQL schema and database objects
- generator/ - modular synthetic data generation scripts
- datasets/ - raw and cleaned datasets
- sql/ - SQL practice exercises by topic
- python/ - Python-based analytics utilities
- pyspark/ - PySpark processing examples
- azure/ - Azure integration notes and templates
- powerbi/ - Power BI modeling and dashboard assets

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
   python3 generator/main.py

## Roadmap

- Phase 1: transactional schema and dataset generation
- Phase 2: SQL analytics and data quality checks
- Phase 3: Azure ingestion and warehousing
- Phase 4: Power BI dashboarding and reporting
