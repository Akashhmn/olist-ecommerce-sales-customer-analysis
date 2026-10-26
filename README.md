# E-Commerce Sales & Customer Analysis

## Project Overview

This project focuses on analyzing sales and customer data from the Olist Brazilian E-Commerce Dataset to derive meaningful business insights.

## Project Objectives

* Analyze e-commerce sales and customer behavior.
* Evaluate order, payment, product, and seller data.
* Identify business trends and performance indicators.
* Develop insights to support data-driven decision-making.

## Dataset

The project uses the Olist Brazilian E-Commerce Dataset, which contains information about orders, customers, products, sellers, payments, and reviews.

The raw and cleaned CSV files are maintained locally and are not included in this repository.

## Project Status

This project is currently **In Progress**.

### Completed

* Project setup and initial data profiling
* Data dictionary and data cleaning strategy
* Table relationship and data quality validation
* Python data cleaning and cleaning validation
* MySQL data import and row-count verification
* SQL business analysis

### In Progress / Planned

* Python exploratory data analysis (EDA) and basic statistics
* Microsoft Excel business analysis and reporting
* Power BI data modeling and dashboard development
* Consolidation of business insights and final project documentation

## SQL Analysis & Selected Findings

SQL analysis was performed using MySQL 8.0 to validate the imported data and investigate sales, customers, products, payments, reviews, and delivery performance.

### Scope of Analysis

* Data validation, row counts, duplicate checks, and table relationships
* Monthly sales trends and order status distribution
* Monthly cancellation rates
* Product category and seller performance
* Customer repeat-purchase behavior
* Payment method distribution and recorded payment value
* Review score distribution
* Delivery performance and late-delivery trends

### Key Findings

* **Payment Methods:** Credit cards accounted for approximately 78.34% of recorded payment value.
* **Customer Retention:** Approximately 3.12% of unique customers placed more than one order in the analyzed dataset.
* **Top Category:** Health and beauty had the highest total item-price sales among the analyzed product categories.
* **Customer Satisfaction:** The average review score was 4.09 out of 5.
* **Delivery Performance:** Approximately 8.11% of eligible delivered orders arrived after the estimated delivery date.

### Interpretation Notes

* Recorded payment value is not the same as profit or final net revenue.
* Product item-price sales exclude freight charges.
* Delivery metrics include only delivered orders with valid purchase, actual delivery, and estimated delivery dates.
* Partial periods in the dataset may affect monthly comparisons.

## Data Import & Technical Notes

Most CSV files were imported directly into MySQL. The `products` and `reviews` tables were imported using Python because the initial direct-import attempts resulted in incomplete row counts. Final row counts were validated after the Python imports.


## Tools & Technologies Used

* **Python** — Data profiling, data quality checks, validation, and data cleaning
* **MySQL 8.0** — Data validation and business analysis using SQL
* **Microsoft Excel** — Business analysis and reporting (planned)
* **Power BI** — Data modeling and dashboard development (planned)

## Project Structure

```text
├── python/          # Python scripts for profiling, validation, cleaning, and MySQL imports
├── sql/             # SQL scripts for data validation and business analysis
├── documentation/   # Data dictionary and data cleaning strategy
├── powerbi/         # Planned location for Power BI project files
├── raw_data/        # Local raw dataset files, excluded from Git
└── cleaned_data/    # Local cleaned dataset files, excluded from Git
```

## Disclaimer

This is an independent portfolio project using the Olist Brazilian E-Commerce Dataset. It is not an official analysis conducted on behalf of Olist.