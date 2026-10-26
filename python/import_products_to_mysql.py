from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, URL, text

csv_path = Path("cleaned_data/products_cleaned.csv")

if not csv_path.exists():
    raise FileNotFoundError(
        f"CSV file not found: {csv_path.resolve()}"
    )

password = getpass("Enter MySQL password: ")

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
    print("Reading CSV file...")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    print(f"CSV rows: {len(df)}")
    print("Importing data into MySQL...")

    df.to_sql(
        name="products_python_import",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM products_python_import")
        ).scalar_one()

    print(f"Import completed. MySQL rows: {count}")

finally:
    engine.dispose()