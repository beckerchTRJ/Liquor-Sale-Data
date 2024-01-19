def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


table1_sql = """
CREATE TABLE IF NOT EXISTS aggregated_data (
    total_gallons REAL,
    year INTEGER,
    month INTEGER
);
"""

table2_sql = """
CREATE TABLE IF NOT EXISTS sample_data (
    invoice_line_no TEXT,
    date TEXT, -- or use TIMESTAMP for datetime fields
    store TEXT,
    name TEXT,
    address TEXT,
    city TEXT,
    zipcode TEXT,
    store_location TEXT, -- or customize based on your data format
    county_number TEXT,
    county TEXT,
    category TEXT,
    category_name TEXT,
    vendor_no TEXT,
    vendor_name TEXT,
    itemno TEXT,
    im_desc TEXT,
    pack INTEGER,
    bottle_volume_ml INTEGER,
    state_bottle_cost REAL,
    state_bottle_retail REAL,
    sale_bottles INTEGER,
    sale_dollars REAL,
    sale_liters REAL,
    sale_gallons REAL
);
"""
