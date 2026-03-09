import sqlite3

conn = sqlite3.connect("medsafe.db")
cursor = conn.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    med1 TEXT,
    med2 TEXT,
    warning TEXT
)
""")

# Data insert
cursor.execute(
"INSERT INTO interactions (med1, med2, warning) VALUES (?, ?, ?)",
("paracetamol","alcohol","Dangerous combination")
)

cursor.execute(
"INSERT INTO interactions (med1, med2, warning) VALUES (?, ?, ?)",
("ibuprofen","aspirin","Risky combination")
)

cursor.execute(
"INSERT INTO interactions (med1, med2, warning) VALUES (?, ?, ?)",
("warfarin","ibuprofen","Severe interaction")
)

conn.commit()
conn.close()

print("Database created and data inserted")