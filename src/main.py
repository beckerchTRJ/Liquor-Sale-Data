from api.soda_client import fetch_data
from db.models import table1_sql, table2_sql
from db.models import create_connection
from db.sqlite_client import create_connection, create_table, insert_data
import pandas as pd
import hashlib
import json

def main():
    # Database setup
    database = "soda_data.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, table1_sql)
        create_table(conn, table2_sql)

        # Fetch and insert aggregated data
        query1 = """
                    SELECT
                        sum(sale_gallons) as total_gallons,
                        date_extract_y(date) as year,
                        date_extract_m(date) as month
                    GROUP BY
                        year, month
                    ORDER BY
                        year, month
                """
        aggregated_data = fetch_data("m3tr-qhgy", query1)
        insert_data(conn, "aggregated_data", pd.DataFrame(aggregated_data))

        # Fetch and insert sample data
        query2 = """SELECT
                        invoice_line_no,
                        date,
                        store,
                        name,
                        address,
                        city,
                        zipcode,
                        store_location,
                        county_number,
                        county,
                        category,
                        category_name,
                        vendor_no,
                        vendor_name,
                        itemno,
                        im_desc,
                        pack,
                        bottle_volume_ml,
                        state_bottle_cost,
                        state_bottle_retail,
                        sale_bottles,
                        sale_dollars,
                        sale_liters,
                        sale_gallons
                    LIMIT 1000"""
        sample_data = fetch_data("m3tr-qhgy", query2)
        sample_data_df = pd.DataFrame(sample_data)
        # Convert columns to appropriate data types
        # Hash the 'invoice_line_no' column using SHA-256
        sample_data_df['invoice_line_no'] = sample_data_df['invoice_line_no'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

        # Convert 'store_location' to a string representation
        sample_data_df['store_location'] = sample_data_df['store_location'].apply(lambda x: json.dumps(x))

        # Remove non-numeric characters from 'sale_dollars' and then convert to float
        # sample_data_df['sale_dollars'] = sample_data_df['sale_dollars'].str.replace(r'[^\d.]', '', regex=True).astype(float)
        # sample_data_df['invoice_line_no'] = sample_data_df['invoice_line_no'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
        sample_data_df['date'] = pd.to_datetime(sample_data_df['date'])
        sample_data_df['store'] = sample_data_df['store'].astype(int)
        sample_data_df['sale_bottles'] = sample_data_df['sale_bottles'].str.replace(',', '').astype(int)
        sample_data_df['sale_dollars'] = sample_data_df['sale_dollars'].str.replace(r'[^\d.]', '', regex=True).astype(float)
        sample_data_df['sale_liters'] = sample_data_df['sale_liters'].astype(float)
        sample_data_df['sale_gallons'] = sample_data_df['sale_gallons'].astype(float)

        sample_data_df.head(10).to_csv('test.csv')
        insert_data(conn, "sample_data", sample_data_df)

        conn.close()

if __name__ == "__main__":
    main()
