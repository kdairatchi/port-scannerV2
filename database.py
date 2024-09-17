import sqlite3

def create_database():
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exploits (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            port INTEGER,
            exploit TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_exploit(ip, port, exploit):
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exploits (ip, port, exploit) VALUES (?, ?, ?)", (ip, port, exploit))
    conn.commit()
    conn.close()

def get_exploits():
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits")
    exploits = cursor.fetchall()
    conn.close()
    return exploits