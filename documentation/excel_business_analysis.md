Excel Business Analysis

1. Objective

Use Microsoft Excel 2021 to perform business-level analysis and validate the outputs generated through Python Exploratory Data Analysis (EDA).

Excel is used to organize selected analytical datasets, calculate business KPIs, summarize important metrics, compare results, and present findings in a structured Business Summary.

The purpose is not to manually clean or process the complete raw dataset in Excel. Python handles the heavier data-processing and analytical tasks, while Excel provides an additional business-analysis and validation layer.

2. Tools and Technologies

- Microsoft Excel 2021: Business analysis, KPI calculations, summary tables, formatting, and data validation.
- Python (Pandas): Preparation and export of selected analytical datasets.
- CSV: Data exchange between Python and Excel.

3. Data Sources

The following seven analytical CSV files were generated using the Python export script:

File Name| Analysis Purpose
monthly_analysis.csv| Monthly payment value and sales trend analysis
category_analysis.csv| Product category performance
customer_analysis.csv| Customer purchasing behaviour
seller_analysis.csv| Seller-level performance
delivery_analysis.csv| Delivery performance and delivery status
review_analysis.csv| Customer review score analysis
payment_analysis.csv| Payment method and payment value analysis

All seven CSV files are stored in the project's "excel/" directory.

The Excel workbook is saved as:

"ollist business analysis.xlsx"

4. Excel Business Analysis

The exported datasets were imported into Microsoft Excel 2021 and converted into structured Excel tables where applicable.

The analysis includes:

- Monthly Analysis: Examination of monthly payment values, average monthly payment, highest monthly payment, and the corresponding month.
- Category Analysis: Comparison of product categories using item volume, order-related metrics, sales value, and average item price.
- Customer Analysis: Examination of unique customers, one-time customers, and repeat customers.
- Seller Analysis: Comparison of seller activity, item volume, and sales value.
- Delivery Analysis: Examination of delivery status, including late and on-time/early deliveries.
- Review Analysis: Examination of customer review scores and rating distribution.
- Payment Analysis: Comparison of payment methods, transaction counts, and recorded payment values.

5. Business Summary

A consolidated Business Summary was prepared to present important business-level metrics and findings in an organized format.

The summary helps interpret the analytical outputs without requiring the reader to examine every individual CSV dataset.

It provides a structured overview of:

- Sales and payment performance.
- Product category performance.
- Customer purchasing behaviour.
- Seller performance.
- Delivery performance.
- Customer review patterns.
- Payment method distribution.

6. Data Validation

Excel was also used as an additional validation layer.

The following checks were performed:

- Verification of imported analytical datasets.
- Validation of important KPI calculations.
- Comparison of summary values against the corresponding Python analytical outputs.
- Checking of monthly trends and missing-month gaps.
- Verification of delivery status counts.
- Checking of customer, seller, review, and payment-related metrics.

The purpose of these checks is to improve consistency between Python-generated outputs and Excel business summaries.

7. Formatting and Presentation

The workbook was formatted to improve readability and professional presentation.

The work included:

- Appropriate number formats for monetary values and percentages.
- Date and time formatting where applicable.
- Structured Excel tables.
- Clear KPI labels and summary values.
- Suitable chart and page layouts.
- Page setup and print formatting.

8. Limitations

- Excel analysis uses selected datasets exported from Python rather than the complete raw dataset.
- The accuracy of Excel summaries depends on the correctness of the source analytical outputs and formulas.
- Recorded payment values and item sales values should not be interpreted as profit.
- The analysis describes observed business patterns and does not independently establish their causes.

9. Status

Completed: Excel Business Analysis, CSV imports, structured tables, KPI calculations, business summary, validation checks, and workbook formatting.

Workbook: "ollist business analysis.xlsx"

Tool: Microsoft Excel 2021

The Excel Business Analysis phase is completed.