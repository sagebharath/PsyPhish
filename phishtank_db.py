import sqlite3

DB = "phishtank.db"

def init_db():
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phishing_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

def insert_urls(urls):
    if not urls:
        return
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        # INSERT OR IGNORE won't crash on duplicates due to UNIQUE constraint on url
        cur.executemany("INSERT OR IGNORE INTO phishing_urls (url) VALUES (?)", [(u,) for u in urls])
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Insert Error: {e}")

def check_url(url):
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM phishing_urls WHERE url=?", (url,))
        r = cur.fetchone()
        conn.close()
        return 1 if r else 0
    except:
        return 0
