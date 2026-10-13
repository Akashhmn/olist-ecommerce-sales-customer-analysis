import pandas as pd
import os

# --------------------------------------------------
# 1. Define the raw data folder
# --------------------------------------------------
data_path = "raw_data"


# --------------------------------------------------
# 2. List datasets included in the quality audit
# --------------------------------------------------
files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
    "reviews": "olist_order_reviews_dataset.csv"
}


# --------------------------------------------------
# 3. Audit each dataset
# --------------------------------------------------
for name, filename in files.items():

    file_path = os.path.join(data_path, filename)
    df = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print(f"DATASET: {name}")

    # Basic structure
    print("\n--- BASIC INFORMATION ---")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Column names
    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    # Data types
    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    # Missing values
    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    # Exact duplicate rows
    print("\n--- EXACT DUPLICATE ROWS ---")
    print(df.duplicated().sum())


print("\n" + "=" * 70)
print("DATA QUALITY AUDIT COMPLETE")