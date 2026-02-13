import sqlite3
import os

def get_db_connection():
     app_dir = os.path.join(os.getenv("LOCALAPPDATA"), "CalculatorAPP")
     if not os.path.exists(app_dir):
          os.mkdir(app_dir)
     db_path = os.path.join(app_dir, "calculator_history.db")
     conn = sqlite3.connect(db_path)
     return conn

def setup_db(conn):
     cursor = conn.cursor()
     cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL)
                    """)
     conn.commit()

def save_history(conn, expr, res):
     cursor = conn.cursor()
     cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expr, str(res)))
     cursor.execute("DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT 20)")
     conn.commit()