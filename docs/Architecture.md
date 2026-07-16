
# Architecture

## Overview

TechMart follows a layered architecture designed for extensibility and future cloud deployment.

1. Data Generation Layer
   - Python scripts generate synthetic transactional data.
2. Raw Data Layer
   - CSV files are stored in datasets/raw for ingestion.
3. Cleansing Layer
   - Intermediate transformations are applied into datasets/cleaned.
4. Analytical Layer
   - Relational schema and warehouse-style views support reporting and BI.
5. Consumption Layer
   - SQL, Python, PySpark, Azure, and Power BI can all consume the same core data model.

## Design Principles

- Modular generation with reusable functions
- Clear separation between source, staging, and warehouse logic
- Industry-standard table and column naming conventions
- Extensible support for large-scale datasets
