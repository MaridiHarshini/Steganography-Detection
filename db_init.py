import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Insert default admin user
c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'Admin@2025', 'admin')")

conn.commit()
conn.close()
print("✅ Database initialized.")

