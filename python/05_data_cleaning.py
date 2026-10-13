import pandas as pd
import os

# ============================================================
# SETUP
# ============================================================

data_path = "raw_data"

# Core datasets required for the project
file_names = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

data = {}

# Load all datasets
for table_name, file_name in file_names.items():
    file_path = os.path.join(data_path, file_name)
    data[table_name] = pd.read_csv(file_path)

print("=" * 60)
print("DATA LOADING COMPLETE")
print("=" * 60)

for table_name, df in data.items():
    print(f"{table_name}: {df.shape[0]} rows, {df.shape[1]} columns")


# ============================================================
# CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES CHECK")
print("=" * 60)

for table_name, df in data.items():
    missing = df.isna().sum()
    missing = missing[missing > 0]

    print(f"\n{table_name}")

    if missing.empty:
        print("No missing values.")
    else:
        print(missing.sort_values(ascending=False).to_string())


# ============================================================
# CHECK DATE COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("DATE COLUMN CHECK")
print("=" * 60)

date_columns = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],
    "reviews": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
}

for table_name, columns in date_columns.items():
    df = data[table_name]

    print(f"\n{table_name}")

    for column in columns:
        print(
            f"{column}: "
            f"{df[column].isna().sum()} missing values; "
            f"current type = {df[column].dtype}"
        )

# ============================================================
# STEP 2: CONVERT DATE COLUMNS TO DATETIME
# ============================================================

print("\n" + "=" * 60)
print("DATE CONVERSION")
print("=" * 60)

for table_name, columns in date_columns.items():
    df = data[table_name]

    for column in columns:
        # Count existing missing values before conversion
        missing_before = df[column].isna().sum()

        # Convert values into datetime format
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        # Count missing values after conversion
        missing_after = df[column].isna().sum()

        # Any increase may indicate invalid date values
        newly_invalid = missing_after - missing_before

        print(
            f"{table_name}.{column}: "
            f"type={df[column].dtype}, "
            f"missing after conversion={missing_after}, "
            f"newly invalid={newly_invalid}"
        )

print("\n" + "=" * 60)
print("PRE-CLEANING CHECK COMPLETE")
print("No rows deleted. No CSV files modified.")
print("=" * 60)

#####
print("\nNUMERIC COLUMN CHECK AND CONVERSION")

numeric_columns = {
    "order_items": [
        "price",
        "freight_value"
    ],
    "payments": [
        "payment_value"
    ],
    "products": [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ],
    "reviews": [
        "review_score"
    ]
}

for table_name, columns in numeric_columns.items():
    df = data[table_name]

    print(f"\nDataset: {table_name}")

    for column in columns:
        missing_before = df[column].isna().sum()

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        missing_after = df[column].isna().sum()
        newly_invalid = missing_after - missing_before

        print(
            f"{column}: "
            f"type={df[column].dtype}, "
            f"missing={missing_after}, "
            f"newly invalid={newly_invalid}"
        )

print("\nNUMERIC COLUMN CHECK COMPLETE")
print("No rows deleted; no CSV files modified.")

#####
print("\nMISSING VALUE PERCENTAGE")

for table_name, df in data.items():
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print(f"\n{table_name}: No missing values")
    else:
        print(f"\n{table_name}")

        for column in missing.index:
            count = missing[column]
            percentage = (count / len(df)) * 100

            print(
                f"{column}: "
                f"{count} missing "
                f"({percentage:.2f}%)"
            )

######
print("\n" + "=" * 60)
print("PRODUCT CATEGORY TRANSLATION")
print("=" * 60)

products = data["products"]
category_translation = data["category_translation"]

products = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

data["products"] = products

print(
    "Products after category translation:",
    data["products"].shape
)

print(
    "Translated categories available:",
    data["products"]["product_category_name_english"].notna().sum()
)

print(
    "Categories without translation:",
    data["products"]["product_category_name_english"].isna().sum()
)

print("\nPRODUCT CATEGORY TRANSLATION COMPLETE")

#####
print("\n" + "=" * 60)
print("HANDLE MISSING CATEGORY TRANSLATIONS")
print("=" * 60)

data["products"]["product_category_name_english"] = (
    data["products"]["product_category_name_english"]
    .fillna("unknown")
)

print(
    "Missing English categories after handling:",
    data["products"]["product_category_name_english"].isna().sum()
)

print("\nMISSING CATEGORY TRANSLATIONS HANDLED")

#####
print("\n" + "=" * 60)
print("EXACT DUPLICATE ROW CHECK")
print("=" * 60)

for table_name, df in data.items():
    duplicate_count = df.duplicated().sum()
    print(f"{table_name}: {duplicate_count} exact duplicate rows")

print("\nEXACT DUPLICATE ROW CHECK COMPLETE")

#####
print("\n" + "=" * 60)
print("LOGICAL CONSISTENCY CHECK")
print("=" * 60)

orders = data["orders"]
order_items = data["order_items"]
payments = data["payments"]
reviews = data["reviews"]

# 1. Order date sequence
invalid_approval = (
    orders["order_approved_at"].notna()
    & (orders["order_approved_at"] < orders["order_purchase_timestamp"])
).sum()

invalid_carrier = (
    orders["order_delivered_carrier_date"].notna()
    & (orders["order_delivered_carrier_date"] < orders["order_purchase_timestamp"])
).sum()

invalid_delivery = (
    orders["order_delivered_customer_date"].notna()
    & (orders["order_delivered_customer_date"] < orders["order_purchase_timestamp"])
).sum()

print(f"Approval before purchase: {invalid_approval}")
print(f"Carrier delivery before purchase: {invalid_carrier}")
print(f"Customer delivery before purchase: {invalid_delivery}")


# 2. Price and freight values
negative_price = (order_items["price"] < 0).sum()
negative_freight = (order_items["freight_value"] < 0).sum()

print(f"Negative prices: {negative_price}")
print(f"Negative freight values: {negative_freight}")


# 3. Payment values
negative_payment = (payments["payment_value"] < 0).sum()

print(f"Negative payment values: {negative_payment}")


# 4. Review score range
invalid_review_score = (
    ~reviews["review_score"].between(1, 5)
).sum()

print(f"Invalid review scores: {invalid_review_score}")


print("\nLOGICAL CONSISTENCY CHECK COMPLETE")

# ============================================================
# HANDLE INVALID CARRIER DELIVERY DATES
# ============================================================

print("\n" + "=" * 60)
print("HANDLE INVALID CARRIER DELIVERY DATES")
print("=" * 60)

invalid_carrier_date = (
    data["orders"]["order_delivered_carrier_date"]
    < data["orders"]["order_purchase_timestamp"]
)

print("Invalid carrier delivery dates found:",
      int(invalid_carrier_date.sum()))

# Keep the orders, but remove the unreliable carrier date
data["orders"].loc[
    invalid_carrier_date,
    "order_delivered_carrier_date"
] = pd.NaT

print(
    "Invalid carrier delivery dates after handling:",
    int(
        (
            data["orders"]["order_delivered_carrier_date"]
            < data["orders"]["order_purchase_timestamp"]
        ).sum()
    )
)

print("Carrier date issue handling complete")

#####
print("\n" + "=" * 60)
print("FINAL CLEANING VALIDATION")
print("=" * 60)

for table_name, df in data.items():
    print(f"\n{table_name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

print("\nFINAL CLEANING VALIDATION COMPLETE")

# ============================================================
# FINAL RAW VS CLEANED REASONABLENESS CHECK
# ============================================================

print("\n" + "=" * 60)
print("RAW VS CLEANED REASONABLENESS CHECK")
print("=" * 60)

raw_data = {
    "orders": 99441,
    "order_items": 112650,
    "payments": 103886,
    "products": 32951,
    "customers": 99441,
    "sellers": 3095,
    "reviews": 99224,
    "category_translation": 71
}

for name, df in data.items():
    raw_rows = raw_data[name]
    cleaned_rows = len(df)

    print(
        f"{name}: "
        f"raw rows={raw_rows}, "
        f"cleaned rows={cleaned_rows}, "
        f"status={'OK' if raw_rows == cleaned_rows else 'CHECK'}"
    )

print("\nRAW VS CLEANED REASONABLENESS CHECK COMPLETE")

# ============================================================
# SAVE CLEANED DATA
# ============================================================

import os

cleaned_data_path = "./cleaned_data"
os.makedirs(cleaned_data_path, exist_ok=True)

for table_name, df in data.items():
    file_path = os.path.join(
        cleaned_data_path,
        f"{table_name}_cleaned.csv"
    )
    df.to_csv(file_path, index=False)

print("\n" + "=" * 60)
print("CLEANED DATA SAVED")
print("=" * 60)

for table_name in data:
    print(f"{table_name}_cleaned.csv")

print("\nCLEANED DATA SAVING COMPLETE")