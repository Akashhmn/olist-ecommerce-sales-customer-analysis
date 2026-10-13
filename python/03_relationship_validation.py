import pandas as pd
import os

# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

data_path = "raw_data"

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

data = {}

for name, filename in files.items():
    data[name] = pd.read_csv(
        os.path.join(data_path, filename)
    )


# --------------------------------------------------
# 2. Primary key / candidate key checks
# --------------------------------------------------

print("\n" + "=" * 65)
print("PRIMARY KEY / CANDIDATE KEY VALIDATION")
print("=" * 65)

key_checks = {
    "orders": ["order_id"],
    "customers": ["customer_id"],
    "products": ["product_id"],
    "sellers": ["seller_id"],
    "order_items": ["order_id", "order_item_id"],
    "payments": ["order_id", "payment_sequential"],
    "category_translation": ["product_category_name"],
    "reviews": ["review_id"]
}

for table, columns in key_checks.items():

    df = data[table]

    missing = df[columns].isnull().any(axis=1).sum()

    duplicates = df.duplicated(
        subset=columns,
        keep=False
    ).sum()

    print(f"\n{table}")
    print("Key columns:", columns)
    print("Rows with missing key values:", missing)
    print("Rows involved in duplicate keys:", duplicates)


# --------------------------------------------------
# 3. Foreign key validation
# --------------------------------------------------

print("\n" + "=" * 65)
print("FOREIGN KEY VALIDATION")
print("=" * 65)

relationships = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("order_items", "seller_id", "sellers", "seller_id"),
    ("payments", "order_id", "orders", "order_id"),
    ("reviews", "order_id", "orders", "order_id"),
    (
        "products",
        "product_category_name",
        "category_translation",
        "product_category_name"
    )
]

for child_table, child_col, parent_table, parent_col in relationships:

    child = data[child_table]
    parent = data[parent_table]

    # Ignore null foreign keys for this unmatched-reference check.
    non_null_values = child[child_col].dropna()

    unmatched = ~non_null_values.isin(
        parent[parent_col]
    )

    print(
        f"\n{child_table}.{child_col} -> "
        f"{parent_table}.{parent_col}"
    )

    print(
        "Non-null foreign key values:",
        len(non_null_values)
    )

    print(
        "Unmatched foreign key rows:",
        int(unmatched.sum())
    )


# --------------------------------------------------
# 4. Review relationship cardinality
# --------------------------------------------------

print("\n" + "=" * 65)
print("RELATIONSHIP CARDINALITY CHECKS")
print("=" * 65)


# --------------------------------------------------
# 4.1 Orders -> Order Items
# --------------------------------------------------

items_per_order = (
    data["order_items"]
    .groupby("order_id")
    .size()
)

print("\nOrder Items per Order")

print(
    "Orders with multiple item rows:",
    int((items_per_order > 1).sum())
)


# --------------------------------------------------
# 4.2 Orders -> Payments
# --------------------------------------------------

payments_per_order = (
    data["payments"]
    .groupby("order_id")
    .size()
)

print("\nPayment Records per Order")

print(
    "Orders with multiple payment rows:",
    int((payments_per_order > 1).sum())
)


# --------------------------------------------------
# 4.3 Customers -> Orders
# --------------------------------------------------

orders_with_customer = data["orders"].merge(
    data["customers"][
        ["customer_id", "customer_unique_id"]
    ],
    on="customer_id",
    how="left"
)

orders_per_customer = (
    orders_with_customer
    .groupby("customer_unique_id")
    .size()
)

print("\nOrders per Customer")

print(
    "Customers with multiple orders:",
    int((orders_per_customer > 1).sum())
)


# --------------------------------------------------
# Validation complete
# --------------------------------------------------

print("\n" + "=" * 65)
print("RELATIONSHIP VALIDATION COMPLETE")
print("=" * 65)