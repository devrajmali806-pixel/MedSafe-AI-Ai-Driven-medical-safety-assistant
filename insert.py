import sqlite3

conn = sqlite3.connect("medsafe.db")
cursor = conn.cursor()

data = [
    ("Paracetamol", "Ibuprofen", "Generally safe but consult doctor"),
    ("Aspirin", "Warfarin", "High bleeding risk"),
    ("Amoxicillin", "Methotrexate", "May increase toxicity"),
    ("Metformin", "Cimetidine", "May increase side effects")
]

cursor.executemany("INSERT INTO interactions (med1, med2, warning) VALUES (?, ?, ?)", data)

conn.commit()
conn.close()

print("Medicine interaction data inserted")