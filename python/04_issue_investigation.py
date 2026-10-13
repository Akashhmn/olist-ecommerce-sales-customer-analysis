import pandas as pd
import os

# ============================================================
# SETUP: LOAD DATA FILES 
# ============================================================

data_path = "raw_data"

reviews = pd.read_csv(
    os.path.join(data_path, "olist_order_reviews_dataset.csv")
)

products = pd.read_csv(
    os.path.join(data_path, "olist_products_dataset.csv")
)

category_translation = pd.read_csv(
    os.path.join(data_path, "product_category_name_translation.csv")
)

customers = pd.read_csv(
    os.path.join(data_path, "olist_customers_dataset.csv")
)


# ============================================================
# INVESTIGATION 1: REVIEW ID CHECK
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATION 1: REVIEW ID CHECK")
print("=" * 60)

# Check missing review IDs
print("\nMissing review_id values:")
print(reviews["review_id"].isna().sum())

# Find all rows whose review_id appears more than once
duplicate_reviews = reviews[
    reviews.duplicated(subset=["review_id"], keep=False)
].sort_values("review_id")

print("\nRows involved in repeated review IDs:")
print(len(duplicate_reviews))

# Count repeated IDs (number of distinct IDs, not rows)
repeated_id_counts = duplicate_reviews["review_id"].value_counts()

print("\nNumber of distinct review IDs that repeat:")
print(len(repeated_id_counts))

print("\nRepeated review IDs and their row counts (top 20):")
print(repeated_id_counts.head(20).to_string())

# Check fully identical rows
print("\nExact duplicate review rows:")
print(reviews.duplicated().sum())

# Show sample records for manual inspection
print("\nSample records with repeated review IDs:")
print(duplicate_reviews.head(10).to_string(index=False))


# ============================================================
# INVESTIGATION 2: PRODUCT CATEGORY CHECK
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATION 2: PRODUCT CATEGORY CHECK")
print("=" * 60)

# Count products whose category is missing
print("\nProducts with missing category:")
print(products["product_category_name"].isna().sum())

# Collect valid category names from the translation table
translated_categories = set(
    category_translation["product_category_name"].dropna()
)

# Find non-null product categories absent from the translation table
unmatched_categories = products.loc[
    products["product_category_name"].notna()
    & ~products["product_category_name"].isin(translated_categories),
    "product_category_name"
]

print("\nProduct rows with unmatched categories:")
print(len(unmatched_categories))

print("\nUnmatched category names and their row counts:")
print(unmatched_categories.value_counts().to_string())


# ============================================================
# INVESTIGATION 3: CUSTOMER ID CHECK
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATION 3: CUSTOMER ID CHECK")
print("=" * 60)

print("\nMissing customer_id values:")
print(customers["customer_id"].isna().sum())

print("\nMissing customer_unique_id values:")
print(customers["customer_unique_id"].isna().sum())

print("\nDistinct non-missing customer_unique_id values:")
print(customers["customer_unique_id"].nunique(dropna=True))


# ============================================================
# FINISH
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATION COMPLETE")
print("=" * 60)