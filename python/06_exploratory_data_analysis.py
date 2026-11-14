from pathlib import Path

import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "cleaned_data"

csv_files = sorted(CLEANED_DATA_DIR.glob("*_cleaned.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No cleaned CSV files found in {CLEANED_DATA_DIR}"
    )

for file_path in csv_files:
    df = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print(f"Dataset: {file_path.name}")
    print("=" * 70)

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    print("\nColumn data types:")
    print(df.dtypes.to_string())

    print("\nMissing values by column:")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0].to_string()
          if missing_values.any() else "No missing values detected.")


# Convert date columns for analysis ---------------------------

orders_file = CLEANED_DATA_DIR / "orders_cleaned.csv"
orders = pd.read_csv(orders_file)

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print("\n" + "=" * 70) 
print("Orders Date Conversion Check")
print("=" * 70)

print(orders[date_columns].dtypes)

print("\nMissing values after date conversion:")
print(orders[date_columns].isnull().sum())


# DESCRIPTIVE STATISTICS ------------------------------
print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)

numeric_columns = {
    "order_items_cleaned.csv": [
        "price",
        "freight_value",
    ],
    "payments_cleaned.csv": [
        "payment_value",
        "payment_installments",
    ],
    "products_cleaned.csv": [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "reviews_cleaned.csv": [
        "review_score",
    ],
}

for file_name, columns in numeric_columns.items():
    file_path = CLEANED_DATA_DIR / file_name
    df = pd.read_csv(file_path)

    print("\n" + "-" * 70)
    print(f"Dataset: {file_name}")
    print("-" * 70)

    print(df[columns].describe().round(2).to_string())

# DATA ANOMALY INVESTIGATION --------------------------------
print("\n" + "=" * 70)
print("DATA ANOMALY INVESTIGATION")
print("=" * 70)

# 1. Investigate order item prices and freight values
items_path = CLEANED_DATA_DIR / "order_items_cleaned.csv"
items_df = pd.read_csv(items_path)

print("\nOrder items with zero freight:")
zero_freight = items_df.loc[items_df["freight_value"] == 0]
print(f"Count: {zero_freight.shape[0]:,}")
print(zero_freight[["order_id", "product_id", "price", "freight_value"]].head(5).to_string(index=False))

print("\nTop 5 item prices:")
print(
    items_df.nlargest(5, "price")[
        ["order_id", "product_id", "price", "freight_value"]
    ].to_string(index=False)
)

print("\nTop 5 freight values:")
print(
    items_df.nlargest(5, "freight_value")[
        ["order_id", "product_id", "price", "freight_value"]
    ].to_string(index=False)
)

# 2. Investigate payment values and installments
payments_path = CLEANED_DATA_DIR / "payments_cleaned.csv"
payments_df = pd.read_csv(payments_path)

print("\nPayment records with zero payment value:")
zero_payments = payments_df.loc[payments_df["payment_value"] == 0]
print(f"Count: {zero_payments.shape[0]:,}")
print(
    zero_payments[
        ["order_id", "payment_sequential", "payment_type",
         "payment_installments", "payment_value"]
    ].head(5).to_string(index=False)
)

print("\nPayment records with zero installments:")
zero_installments = payments_df.loc[payments_df["payment_installments"] == 0]
print(f"Count: {zero_installments.shape[0]:,}")
print(
    zero_installments[
        ["order_id", "payment_sequential", "payment_type",
         "payment_installments", "payment_value"]
    ].head(5).to_string(index=False)
)

# 3. Investigate product weights
products_path = CLEANED_DATA_DIR / "products_cleaned.csv"
products_df = pd.read_csv(products_path)

print("\nProducts with zero weight:")
zero_weight = products_df.loc[products_df["product_weight_g"] == 0]
print(f"Count: {zero_weight.shape[0]:,}")
print(
    zero_weight[
        ["product_id", "product_category_name_english",
         "product_weight_g", "product_length_cm",
         "product_height_cm", "product_width_cm"]
    ].head(5).to_string(index=False)
)

print("\nTop 5 product weights:")
print(
    products_df.nlargest(5, "product_weight_g")[
        ["product_id", "product_category_name_english",
         "product_weight_g", "product_length_cm",
         "product_height_cm", "product_width_cm"]
    ].to_string(index=False)
)

# CATEGORICAL DISTRIBUTIONS ------------------------
print("\n" + "=" * 70)
print("CATEGORICAL DISTRIBUTIONS")
print("=" * 70)

categorical_checks = {
    "orders_cleaned.csv": [
        "order_status",
    ],
    "payments_cleaned.csv": [
        "payment_type",
    ],
    "products_cleaned.csv": [
        "product_category_name_english",
    ],
    "customers_cleaned.csv": [
        "customer_state",
    ],
    "sellers_cleaned.csv": [
        "seller_state",
    ],
}

for file_name, columns in categorical_checks.items():
    file_path = CLEANED_DATA_DIR / file_name
    df = pd.read_csv(file_path)

    for column in columns:
        print("\n" + "-" * 70)
        print(f"Dataset: {file_name} | Column: {column}")
        print("-" * 70)

        counts = df[column].fillna("Missing").value_counts()

        print(f"Unique categories: {df[column].nunique(dropna=True):,}")
        print(counts.head(10).to_string())


# ==========================================
# 1. MONTHLY SALES TREND ANALYSIS
# ==========================================

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from pathlib import Path
import pandas as pd

# Load orders and payments data
orders = pd.read_csv("cleaned_data/orders_cleaned.csv")
payments = pd.read_csv("cleaned_data/payments_cleaned.csv")

# Convert purchase timestamp into datetime format
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Calculate total payment value for each order
order_payments = payments.groupby(
    "order_id", as_index=False
)["payment_value"].sum()

# Merge order dates with aggregated payment values
sales_data = orders[
    ["order_id", "order_purchase_timestamp"]
].merge(
    order_payments,
    on="order_id",
    how="inner"
)

# Extract purchase month
sales_data["purchase_month"] = (
    sales_data["order_purchase_timestamp"].dt.to_period("M")
)

# Calculate monthly sales value
monthly_sales = sales_data.groupby(
    "purchase_month"
)["payment_value"].sum().reset_index()

# Create a complete monthly date range
all_months = pd.period_range(
    start=monthly_sales["purchase_month"].min(),
    end=monthly_sales["purchase_month"].max(),
    freq="M"
)

# Include missing months as NaN, not zero
monthly_sales = (
    monthly_sales.set_index("purchase_month")
    .reindex(all_months)
    .rename_axis("purchase_month")
    .reset_index()
)

# Display monthly sales including missing months
monthly_sales["purchase_month"] = (
    monthly_sales["purchase_month"].astype(str)
)

print("\nMONTHLY SALES TREND")
print(monthly_sales.to_string(index=False))

# Create visualization folder
visualization_dir = Path("visualizations")
visualization_dir.mkdir(exist_ok=True)

# Plot monthly sales
plt.figure(figsize=(14, 6))

plt.plot(
    monthly_sales["purchase_month"],
    monthly_sales["payment_value"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Purchase Month")
plt.ylabel("Total Payment Value")

# Format Y-axis with comma-separated values
plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
plt.savefig(
    visualization_dir / "monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 2. ORDER TRENDS ANALYSIS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import StrMethodFormatter

# Load orders data
orders = pd.read_csv("cleaned_data/orders_cleaned.csv")

# Convert purchase timestamps to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# Keep orders with valid purchase timestamps
valid_orders = orders.dropna(
    subset=["order_purchase_timestamp"]
).copy()

# Extract purchase month
valid_orders["order_month"] = (
    valid_orders["order_purchase_timestamp"].dt.to_period("M")
)

# Count orders placed in each month
monthly_orders = (
    valid_orders.groupby("order_month")["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

# Include all months in the observed date range
all_months = pd.period_range(
    start=monthly_orders["order_month"].min(),
    end=monthly_orders["order_month"].max(),
    freq="M"
)

monthly_orders = (
    monthly_orders.set_index("order_month")
    .reindex(all_months)
    .rename_axis("order_month")
    .reset_index()
)

# Display monthly order counts
print("\nMONTHLY ORDER TRENDS")
print(monthly_orders.to_string(index=False))

# Prepare output folder
visualization_dir = Path("visualizations")
visualization_dir.mkdir(exist_ok=True)

# Plot monthly order volume
plt.figure(figsize=(14, 6))

plt.plot(
    monthly_orders["order_month"].astype(str),
    monthly_orders["total_orders"],
    marker="o"
)

plt.title("Monthly Order Trends")
plt.xlabel("Purchase Month")
plt.ylabel("Number of Orders")

plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the chart without replacing the sales chart
plt.savefig(
    visualization_dir / "monthly_order_trend.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 3. CATEGORY PERFORMANCE ANALYSIS
# ==========================================

# Load required datasets
order_items = pd.read_csv("cleaned_data/order_items_cleaned.csv")
products = pd.read_csv("cleaned_data/products_cleaned.csv")

# Keep only the required product columns
product_categories = products[
    ["product_id", "product_category_name_english"]
]

# Merge order items with product categories
category_data = order_items.merge(
    product_categories,
    on="product_id",
    how="left"
)

# Group data by product category
category_performance = (
    category_data
    .groupby("product_category_name_english")
    .agg(
        total_items=("order_item_id", "count"),
        total_orders=("order_id", "nunique"),
        total_sales=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .reset_index()
)

# Sort categories by total sales
category_performance = category_performance.sort_values(
    by="total_sales",
    ascending=False
)

# Round monetary values
category_performance[
    ["total_sales", "average_item_price"]
] = category_performance[
    ["total_sales", "average_item_price"]
].round(2)

# Display top 10 categories
print("\nCATEGORY PERFORMANCE")
print(category_performance.head(10).to_string(index=False))

# ==========================================
# CATEGORY PERFORMANCE VISUALIZATION
# ==========================================

# Select top 10 categories by sales value
top_sales_categories = category_performance.nlargest(
    10, "total_sales"
).sort_values("total_sales", ascending=True)

# Create sales value chart
plt.figure(figsize=(12, 7))

plt.barh(
    top_sales_categories["product_category_name_english"],
    top_sales_categories["total_sales"]
)

plt.title("Top 10 Product Categories by Sales Value")
plt.xlabel("Total Sales Value")
plt.ylabel("Product Category")
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.tight_layout()

plt.savefig(
    visualization_dir / "top_categories_by_sales.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()


# Select top 10 categories by items sold
top_item_categories = category_performance.nlargest(
    10, "total_items"
).sort_values("total_items", ascending=True)

# Create item quantity chart
plt.figure(figsize=(12, 7))

plt.barh(
    top_item_categories["product_category_name_english"],
    top_item_categories["total_items"]
)

plt.title("Top 10 Product Categories by Items Sold")
plt.xlabel("Total Items Sold")
plt.ylabel("Product Category")

plt.tight_layout()

plt.savefig(
    visualization_dir / "top_categories_by_items.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 4. CUSTOMER BEHAVIOUR ANALYSIS
# ==========================================

# Load required datasets
orders = pd.read_csv("cleaned_data/orders_cleaned.csv")
customers = pd.read_csv("cleaned_data/customers_cleaned.csv")

# Select required customer information
customer_details = customers[
    ["customer_id", "customer_unique_id"]
]

# Merge orders with unique customer identifiers
customer_orders = orders.merge(
    customer_details,
    on="customer_id",
    how="left"
)

# Remove records with missing customer identifiers
customer_orders = customer_orders.dropna(
    subset=["customer_unique_id"]
)

# Calculate total unique orders for each customer
customer_frequency = (
    customer_orders
    .groupby("customer_unique_id")["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

# Create customer order frequency distribution
frequency_distribution = (
    customer_frequency
    .groupby("total_orders")
    .size()
    .reset_index(name="customer_count")
)

# Calculate percentage of customers in each frequency group
frequency_distribution["customer_percentage"] = (
    frequency_distribution["customer_count"]
    / frequency_distribution["customer_count"].sum()
    * 100
).round(2)

# Calculate overall customer frequency statistics
print("\nCUSTOMER ORDER FREQUENCY STATISTICS")
print(customer_frequency["total_orders"].describe())

# Display customer order frequency distribution
print("\nCUSTOMER ORDER FREQUENCY DISTRIBUTION")
print(frequency_distribution.to_string(index=False))

# Calculate one-time and repeat customer summary
one_time_customers = (
    customer_frequency["total_orders"] == 1
).sum()

repeat_customers = (
    customer_frequency["total_orders"] > 1
).sum()

total_customers = len(customer_frequency)

print("\nONE-TIME VS REPEAT CUSTOMERS")
print(f"Total Customers: {total_customers}")
print(f"One-Time Customers: {one_time_customers}")
print(f"Repeat Customers: {repeat_customers}")
print(
    f"One-Time Customer Percentage: "
    f"{one_time_customers / total_customers * 100:.2f}%"
)
print(
    f"Repeat Customer Percentage: "
    f"{repeat_customers / total_customers * 100:.2f}%"
)

# ==========================================
# CUSTOMER BEHAVIOUR VISUALIZATION
# ==========================================

# Create visualization folder if it does not exist
visualization_dir = Path("visualizations")
visualization_dir.mkdir(exist_ok=True)

# Chart : Order Frequency Among Repeat Customers
repeat_frequency = frequency_distribution[
    frequency_distribution["total_orders"] > 1
].copy()

plt.figure(figsize=(10, 6))

plt.bar(
    repeat_frequency["total_orders"].astype(str),
    repeat_frequency["customer_count"]
)

plt.title("Order Frequency Among Repeat Customers")
plt.xlabel("Number of Orders per Customer")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    visualization_dir / "repeat_customer_order_frequency.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 5. SELLER PERFORMANCE ANALYSIS
# ==========================================

order_items = pd.read_csv("cleaned_data/order_items_cleaned.csv")
sellers = pd.read_csv("cleaned_data/sellers_cleaned.csv")

seller_data = order_items.merge(
    sellers[["seller_id", "seller_state"]],
    on="seller_id",
    how="left"
)

seller_performance = (
    seller_data
    .groupby("seller_id")
    .agg(
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count"),
        total_sales=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .reset_index()
)

seller_performance = seller_performance.sort_values(
    by="total_sales",
    ascending=False
)

seller_performance[
    ["total_sales", "average_item_price"]
] = seller_performance[
    ["total_sales", "average_item_price"]
].round(2)

print("\nTOP 10 SELLERS BY SALES VALUE")
print(seller_performance.head(10).to_string(index=False))

print("\nSELLER PERFORMANCE STATISTICS")
print(
    seller_performance[
        ["total_orders", "total_items", "total_sales", "average_item_price"]
    ].describe().round(2)
)

# ==========================================
# SELLER PERFORMANCE VISUALIZATION
# ==========================================

top_sellers = (
    seller_performance
    .head(10)
    .sort_values("total_sales", ascending=True)
    .copy()
)

top_sellers["seller_label"] = (
    top_sellers["seller_id"].str[:8]
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_sellers["seller_label"],
    top_sellers["total_sales"]
)

plt.title("Top 10 Sellers by Sales Value")
plt.xlabel("Total Sales Value")
plt.ylabel("Seller ID")

plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.tight_layout()

plt.savefig(
    visualization_dir / "top_sellers_by_sales.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 6. DELIVERY TIME ANALYSIS
# ==========================================

orders = pd.read_csv("cleaned_data/orders_cleaned.csv")

# Convert date columns into datetime format
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

# Keep delivered orders with valid delivery dates
delivery_data = orders[
    (orders["order_status"] == "delivered")
    & (orders["order_purchase_timestamp"].notna())
    & (orders["order_delivered_customer_date"].notna())
    & (orders["order_estimated_delivery_date"].notna())
].copy()

# Calculate actual and estimated delivery duration
delivery_data["actual_delivery_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.total_seconds() / 86400

delivery_data["estimated_delivery_days"] = (
    delivery_data["order_estimated_delivery_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate difference between actual and estimated delivery dates
delivery_data["delivery_difference_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# Classify delivery performance
delivery_data["delivery_status"] = np.where(
    delivery_data["delivery_difference_days"] > 0,
    "Late",
    "On-time/Early"
)

# Descriptive statistics
print("\nDELIVERY TIME STATISTICS")

print(
    delivery_data[
        [
            "actual_delivery_days",
            "estimated_delivery_days",
            "delivery_difference_days"
        ]
    ].describe().round(2)
)

# Delivery status distribution
delivery_status_distribution = (
    delivery_data["delivery_status"]
    .value_counts()
    .reset_index()
)

delivery_status_distribution.columns = [
    "delivery_status",
    "order_count"
]

delivery_status_distribution["percentage"] = (
    delivery_status_distribution["order_count"]
    / len(delivery_data) * 100
).round(2)

print("\nDELIVERY STATUS DISTRIBUTION")
print(delivery_status_distribution.to_string(index=False))

# Average delivery duration by delivery status
print("\nAVERAGE DELIVERY TIME BY STATUS")

print(
    delivery_data.groupby("delivery_status")[
        ["actual_delivery_days", "delivery_difference_days"]
    ].mean().round(2)
)

# MONTHLY DELIVERY TIME ANALYSIS

delivery_data["purchase_month"] = (
    delivery_data["order_purchase_timestamp"].dt.to_period("M")
)

monthly_delivery = (
    delivery_data
    .groupby("purchase_month")
    .agg(
        total_orders=("order_id", "nunique"),
        average_actual_days=("actual_delivery_days", "mean"),
        average_estimated_days=("estimated_delivery_days", "mean")
    )
    .reset_index()
)

print("\nMONTHLY DELIVERY TIME SUMMARY")
print(monthly_delivery.round(2).to_string(index=False))

# ==========================================
# DELIVERY TIME VISUALIZATION
# ==========================================

delivery_data["purchase_month"] = (
    delivery_data["order_purchase_timestamp"].dt.to_period("M")
)

monthly_delivery = (
    delivery_data
    .groupby("purchase_month")
    .agg(
        average_actual_days=("actual_delivery_days", "mean"),
        average_estimated_days=("estimated_delivery_days", "mean")
    )
    .reset_index()
)

monthly_delivery["purchase_month"] = (
    monthly_delivery["purchase_month"].astype(str)
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_delivery["purchase_month"],
    monthly_delivery["average_actual_days"],
    marker="o",
    label="Average Actual Delivery Days"
)

plt.plot(
    monthly_delivery["purchase_month"],
    monthly_delivery["average_estimated_days"],
    marker="o",
    label="Average Estimated Delivery Days"
)

plt.title("Monthly Actual vs Estimated Delivery Time")
plt.xlabel("Purchase Month")
plt.ylabel("Average Delivery Days")
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "visualizations/monthly_delivery_time_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 7. REVIEW SCORES ANALYSIS
# ==========================================

reviews = pd.read_csv("cleaned_data/reviews_cleaned.csv")

review_scores = reviews["review_score"].dropna()

print("\nREVIEW SCORE STATISTICS")
print(review_scores.describe().round(2))

review_distribution = (
    review_scores.value_counts()
    .sort_index()
    .reset_index()
)

review_distribution.columns = ["review_score", "review_count"]

review_distribution["percentage"] = (
    review_distribution["review_count"]
    / review_distribution["review_count"].sum() * 100
).round(2)

print("\nREVIEW SCORE DISTRIBUTION")
print(review_distribution.to_string(index=False))

positive_percentage = (
    review_distribution.loc[
        review_distribution["review_score"].isin([4, 5]),
        "percentage"
    ].sum()
)

low_percentage = (
    review_distribution.loc[
        review_distribution["review_score"].isin([1, 2]),
        "percentage"
    ].sum()
)

print("\nREVIEW SCORE SUMMARY")
print(f"Positive Ratings (4-5): {positive_percentage:.2f}%")
print(f"Low Ratings (1-2): {low_percentage:.2f}%")

# ==========================================
# REVIEW SCORE VISUALIZATION
# ==========================================

visualization_dir = Path("visualizations")
visualization_dir.mkdir(exist_ok=True)

plt.figure(figsize=(9, 6))

bars = plt.bar(
    review_distribution["review_score"].astype(str),
    review_distribution["percentage"]
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Percentage of Reviews")

for bar, percentage in zip(bars, review_distribution["percentage"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{percentage:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    visualization_dir / "review_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()

# ==========================================
# 8. PAYMENT BEHAVIOUR ANALYSIS
# ==========================================

payments = pd.read_csv("cleaned_data/payments_cleaned.csv")

payment_summary = (
    payments
    .groupby("payment_type")
    .agg(
        transaction_count=("order_id", "count"),
        total_payment_value=("payment_value", "sum"),
        average_payment_value=("payment_value", "mean")
    )
    .reset_index()
)

total_value = payment_summary["total_payment_value"].sum()

payment_summary["payment_value_percentage"] = (
    payment_summary["total_payment_value"] / total_value * 100
).round(2)

payment_summary = payment_summary.sort_values(
    by="total_payment_value",
    ascending=False
)

payment_summary[
    ["total_payment_value", "average_payment_value"]
] = payment_summary[
    ["total_payment_value", "average_payment_value"]
].round(2)

print("\nPAYMENT BEHAVIOUR ANALYSIS")
print(payment_summary.to_string(index=False))

print("\nPAYMENT SUMMARY STATISTICS")
print(payments["payment_value"].describe().round(2))

# ==========================================
# PAYMENT BEHAVIOUR VISUALIZATION
# ==========================================

visualization_dir = Path("visualizations")
visualization_dir.mkdir(exist_ok=True)

payment_chart_data = payment_summary[
    payment_summary["payment_type"] != "not_defined"
].sort_values("payment_value_percentage")

plt.figure(figsize=(9, 6))

bars = plt.barh(
    payment_chart_data["payment_type"],
    payment_chart_data["payment_value_percentage"]
)

plt.title("Payment Value Share by Payment Method")
plt.xlabel("Percentage of Total Payment Value")
plt.ylabel("Payment Method")

for bar, percentage in zip(
    bars, payment_chart_data["payment_value_percentage"]
):
    plt.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{percentage:.2f}%",
        va="center"
    )

plt.xlim(0, 90)
plt.tight_layout()

plt.savefig(
    visualization_dir / "payment_method_value_share.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()
plt.close()