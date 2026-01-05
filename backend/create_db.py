import sqlite3

# Database create / connect
conn = sqlite3.connect("database.db")

# Cursor create
cursor = conn.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database and users table created successfully!")
