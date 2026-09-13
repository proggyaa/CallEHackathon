import sqlite3
from datetime import datetime

conn = sqlite3.connect("listings.db")
cursor = conn.cursor()

# Drop existing table to ensure a fresh schema build
cursor.execute("DROP TABLE IF EXISTS listings")

# Recreate table including called_at column
cursor.execute("""
    CREATE TABLE listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        broker_name TEXT,
        broker_contact TEXT,
        rent TEXT,
        called_at DATETIME
    )
""")

# Sample demo data matching the sanitized batch results addresses
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sample_listings = [
    ("101 Example Street, Sample District", "Sample Broker One", "+15550001001", "45,000", now),
    ("202 Example Avenue, Sample District", "Sample Broker Two", "+15550001002", "52,000", now),
    ("303 Example Road, Sample District", "Sample Broker Three", "+15550001003", "60,000", now)
]

cursor.executemany("""
    INSERT INTO listings (address, broker_name, broker_contact, rent, called_at)
    VALUES (?, ?, ?, ?, ?)
""", sample_listings)

conn.commit()
conn.close()

print("[+] listings.db successfully populated with fresh demo data containing 'called_at'!")