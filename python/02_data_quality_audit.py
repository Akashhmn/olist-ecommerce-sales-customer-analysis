
import pandas as pd
import os

# 1. Define the data folder
data_path = "raw_data"

# 2. List the seven core datasets
files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# 3. Audit each dataset
for name, filename in files.items():
    file_path = os.path.join(data_path, filename)
    df = pd.read_csv(file_path)

    print("\n" + "=" * 60)
    print("DATASET:", name)
    print("ROWS:", df.shape[0])
    print("COLUMNS:", df.shape[1])

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    print("\nEXACT DUPLICATE ROWS:", df.duplicated().sum())

    print("\nCOLUMN NAMES:")
    print(df.columns.tolist())

print("\nAUDIT COMPLETE")