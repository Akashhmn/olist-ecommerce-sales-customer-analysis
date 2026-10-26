import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, URL, text

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "cleaned_data" / "reviews_cleaned.csv"

# MySQL connection
password = getpass.getpass("Enter MySQL password : ")

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="olist_ecommerce",
)

engine = create_engine(url)

try:
    # Check CSV
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"not findCSV file: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    print("CSV rows:", len(df))
    print("CSV columns:", list(df.columns))

    # Safety: don't overwrite any existing table
    with engine.connect() as conn:
        existing = conn.execute(text("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'olist_ecommerce'
              AND table_name = 'reviews_python_import'
        """)).scalar()

    if existing:
        raise RuntimeError(
            "reviews_python_import table pehle se maujood hai. "
            "Koi data overwrite nahi kiya gaya."
        )

    # Import to a new table
    df.to_sql(
        name="reviews_python_import",
        con=engine,
        if_exists="fail",
        index=False,
        chunksize=1000,
        method="multi",
    )

    # Verify
    with engine.connect() as conn:
        sql_count = conn.execute(
            text("SELECT COUNT(*) FROM reviews_python_import")
        ).scalar()

    print("MySQL imported rows:", sql_count)

    if sql_count == len(df):
        print("SUCCESS: CSV aur MySQL row counts match!")
    else:
        print("WARNING: CSV aur MySQL row counts match nahi karte.")

finally:
    engine.dispose()