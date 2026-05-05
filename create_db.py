import sqlite3
import csv

conn = sqlite3.connect("cemetery.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS graves")

cursor.execute("""
CREATE TABLE graves (
    record_id INTEGER PRIMARY KEY,
    full_name TEXT,
    birth_date TEXT,
    death_date TEXT,
    section TEXT,
    plot_number TEXT,
    latitude REAL,
    longitude REAL,
    veteran_status TEXT,
    headstone_condition TEXT,
    photo_file TEXT,
    notes TEXT
)
""")


with open("greenwood.csv", newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
            INSERT INTO graves (
                record_id, full_name, birth_date, death_date,
                section, plot_number, latitude, longitude,
                veteran_status, headstone_condition, photo_file, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["record_id"],
            row["full_name"],
            row["birth_date"],
            row["death_date"],
            row["section"],
            row["plot_number"],
            row["latitude"],
            row["longitude"],
            row["veteran_status"],
            row["headstone_condition"],
            row["photo_file"],
            row["notes"]
        ))

conn.commit()
conn.close()

print("Greenwood CSV imported into cemetery.db successfully!")