import pandas as pd
from pathlib import Path

# Project directories
project_root = Path(__file__).resolve().parent.parent
cleaned_data_dir = project_root / "cleaned_data"
excel_dir = project_root / "excel"

# Create the Excel output folder if it does not exist
excel_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# MONTHLY ANALYSIS EXPORT
# --------------------------------------------------

# Load cleaned datasets
orders = pd.read_csv(cleaned_data_dir / "orders_cleaned.csv")
payments = pd.read_csv(cleaned_data_dir / "payments_cleaned.csv")

# Convert purchase timestamps to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# Aggregate payment values at order level
payment_by_order = (
    payments.groupby("order_id", as_index=False)
    .agg(total_payment_value=("payment_value", "sum"))
)

# Join order-level payments with purchase dates
sales_data = orders[
    ["order_id", "order_purchase_timestamp"]
].merge(
    payment_by_order,
    on="order_id",
    how="inner"
)

# Extract purchase month
sales_data["purchase_month"] = (
    sales_data["order_purchase_timestamp"].dt.to_period("M")
)

# Calculate monthly payment values
monthly_sales = (
    sales_data.groupby("purchase_month")["total_payment_value"]
    .sum()
)

# Include missing months as blank values, not zero
all_months = pd.period_range(
    start=monthly_sales.index.min(),
    end=monthly_sales.index.max(),
    freq="M"
)

monthly_sales = monthly_sales.reindex(all_months)

# Prepare the Excel-ready summary
monthly_analysis = monthly_sales.rename(
    "payment_value"
).reset_index()

monthly_analysis = monthly_analysis.rename(
    columns={"index": "purchase_month"}
)

monthly_analysis["purchase_month"] = (
    monthly_analysis["purchase_month"].astype(str)
)

# Export the summary as CSV
output_path = excel_dir / "monthly_analysis.csv"

monthly_analysis.to_csv(
    output_path,
    index=False,
    float_format="%.2f"
)

print("Monthly sales summary exported successfully.")
print(monthly_analysis.to_string(index=False))
print(f"\nFile saved at: {output_path}")

# --------------------------------------------------
# CATEGORY ANALYSIS EXPORT
# --------------------------------------------------

# Load required cleaned datasets
order_items = pd.read_csv(
    cleaned_data_dir / "order_items_cleaned.csv"
)

products = pd.read_csv(
    cleaned_data_dir / "products_cleaned.csv"
)

category_translation = pd.read_csv(
    cleaned_data_dir / "category_translation_cleaned.csv"
)

# Select required product information
product_categories = products[
    ["product_id", "product_category_name"]
].merge(
    category_translation[
        ["product_category_name", "product_category_name_english"]
    ],
    on="product_category_name",
    how="left"
)

# Combine order items with product categories
category_analysis = order_items.merge(
    product_categories[
        ["product_id", "product_category_name_english"]
    ],
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Select final Excel analysis columns
category_analysis = category_analysis[
    [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "product_category_name_english",
        "price",
        "freight_value"
    ]
]

# Export category analysis data
category_output_path = excel_dir / "category_analysis.csv"

category_analysis.to_csv(
    category_output_path,
    index=False,
    float_format="%.2f"
)

print("\nCategory analysis exported successfully.")
print(f"Total order-item rows: {len(category_analysis)}")
print(f"File saved at: {category_output_path}")

# --------------------------------------------------
# CUSTOMER ANALYSIS EXPORT
# --------------------------------------------------

# Load customer and order data
customers = pd.read_csv(
    cleaned_data_dir / "customers_cleaned.csv"
)

orders = pd.read_csv(
    cleaned_data_dir / "orders_cleaned.csv"
)

# Join orders with customer identities
customer_orders = orders[
    ["order_id", "customer_id", "order_purchase_timestamp"]
].merge(
    customers[
        ["customer_id", "customer_unique_id"]
    ],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# Convert purchase timestamp to datetime
customer_orders["order_purchase_timestamp"] = pd.to_datetime(
    customer_orders["order_purchase_timestamp"],
    errors="coerce"
)

# Aggregate order information by unique customer
customer_analysis = (
    customer_orders
    .groupby("customer_unique_id", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        first_order_date=("order_purchase_timestamp", "min"),
        last_order_date=("order_purchase_timestamp", "max")
    )
)

# Classify customers by order frequency
customer_analysis["customer_type"] = customer_analysis[
    "total_orders"
].apply(
    lambda count: "Repeat" if count > 1 else "One-time"
)

# Export customer analysis data
customer_output_path = excel_dir / "customer_analysis.csv"

customer_analysis.to_csv(
    customer_output_path,
    index=False
)

print("\nCustomer analysis exported successfully.")
print(f"Total unique customers: {len(customer_analysis)}")
print("Repeat customers:",(customer_analysis["customer_type"] == "Repeat").sum())
print("One-time customers:",(customer_analysis["customer_type"] == "One-time").sum())
print(f"File saved at: {customer_output_path}")

# --------------------------------------------------
# SELLER ANALYSIS EXPORT
# --------------------------------------------------

# Load order-item data
order_items = pd.read_csv(
    cleaned_data_dir / "order_items_cleaned.csv"
)

# Aggregate performance by seller
seller_analysis = (
    order_items
    .groupby("seller_id", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_items_sold=("order_item_id", "count"),
        total_sales=("price", "sum"),
        total_freight=("freight_value", "sum"),
        average_item_price=("price", "mean")
    )
)

# Export seller analysis data
seller_output_path = excel_dir / "seller_analysis.csv"

seller_analysis.to_csv(
    seller_output_path,
    index=False,
    float_format="%.2f"
)

print("\nSeller analysis exported successfully.")
print(f"Total sellers: {len(seller_analysis)}")
print(f"Total items sold: {seller_analysis['total_items_sold'].sum()}")
print(f"Total sales: {seller_analysis['total_sales'].sum():.2f}")
print(f"File saved at: {seller_output_path}")

# --------------------------------------------------
# DELIVERY ANALYSIS EXPORT
# --------------------------------------------------

# Load order data
orders = pd.read_csv(
    cleaned_data_dir / "orders_cleaned.csv"
)

# Convert delivery timestamps
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

# Keep delivered orders with all required dates
delivery_analysis = orders[
    orders["order_status"].eq("delivered")
    & orders[date_columns].notna().all(axis=1)
].copy()

# Calculate delivery durations
delivery_analysis["actual_delivery_days"] = (
    delivery_analysis["order_delivered_customer_date"]
    - delivery_analysis["order_purchase_timestamp"]
).dt.total_seconds() / 86400

delivery_analysis["estimated_delivery_days"] = (
    delivery_analysis["order_estimated_delivery_date"]
    - delivery_analysis["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate delivery delay
delivery_analysis["delivery_delay_days"] = (
    delivery_analysis["actual_delivery_days"]
    - delivery_analysis["estimated_delivery_days"]
)

# Classify delivery performance
delivery_analysis["delivery_status"] = (
    delivery_analysis["delivery_delay_days"]
    .apply(
        lambda days: "Late" if days > 0 else "On-time/Early"
    )
)

# Extract purchase month
delivery_analysis["purchase_month"] = (
    delivery_analysis["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

# Select final columns
delivery_analysis = delivery_analysis[
    [
        "order_id",
        "purchase_month",
        "actual_delivery_days",
        "estimated_delivery_days",
        "delivery_delay_days",
        "delivery_status",
        "order_purchase_timestamp"
    ]
]

# Export delivery analysis data
delivery_output_path = excel_dir / "delivery_analysis.csv"

delivery_analysis.to_csv(
    delivery_output_path,
    index=False,
    float_format="%.2f"
)

print("\nDelivery analysis exported successfully.")
print(f"Delivered orders analyzed: {len(delivery_analysis)}")
print("Late deliveries:",(delivery_analysis["delivery_status"] == "Late").sum())
print("On-time/Early deliveries:",(delivery_analysis["delivery_status"] == "On-time/Early").sum())
print(f"File saved at: {delivery_output_path}")

# --------------------------------------------------
# REVIEW ANALYSIS EXPORT
# --------------------------------------------------

# Load review data
reviews = pd.read_csv(
    cleaned_data_dir / "reviews_cleaned.csv"
)

# Convert review timestamps
review_date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in review_date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

# Select final analysis columns
review_analysis = reviews[
    [
        "review_id",
        "order_id",
        "review_score",
        "review_creation_date",
        "review_answer_timestamp"
    ]
].copy()

# Export review analysis data
review_output_path = excel_dir / "review_analysis.csv"

review_analysis.to_csv(
    review_output_path,
    index=False
)

print("\nReview analysis exported successfully.")
print(f"Total review records: {len(review_analysis)}")
print("Average review score:",f"{review_analysis['review_score'].mean():.2f}")
print("Missing review scores:", review_analysis["review_score"].isna().sum())
print(f"File saved at: {review_output_path}")

# --------------------------------------------------
# PAYMENT ANALYSIS EXPORT
# --------------------------------------------------

# Load payment data
payments = pd.read_csv(
    cleaned_data_dir / "payments_cleaned.csv"
)

# Select final analysis columns
payment_analysis = payments[
    [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]
].copy()

# Export payment analysis data
payment_output_path = excel_dir / "payment_analysis.csv"

payment_analysis.to_csv(
    payment_output_path,
    index=False,
    float_format="%.2f"
)

print("\nPayment analysis exported successfully.")
print(f"Total payment records: {len(payment_analysis)}")
print("Total recorded payment value:",f"{payment_analysis['payment_value'].sum():.2f}")
print(f"File saved at: {payment_output_path}")