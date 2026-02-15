import sqlite3
import os

class DatabaseManager: 
     def __init__(self):
          app_dir = os.path.join(os.getenv("LOCALAPPDATA"), "CalculatorAPP")
          os.makedirs(app_dir, exist_ok=True)
          self.db_path = os.path.join(app_dir, "calculator_history.db")
          self.conn = sqlite3.connect(self.db_path)
          self.setup_db()

     def setup_db(self):
          cursor = self.conn.cursor()
          cursor.execute("""
                         CREATE TABLE IF NOT EXISTS history(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         expression TEXT NOT NULL,
                         result TEXT NOT NULL)
                         """)
          self.conn.commit()

     def save(self, expr, result):
          cursor = self.conn.cursor()
          cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expr, str(result)))
          cursor.execute("DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT 20)")
          self.conn.commit()

     def fetch_all(self):
          cursor = self.conn.cursor()
          cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
          return cursor.fetchall()

     def clear(self):
          cursor = self.conn.cursor()
          cursor.execute("DELETE FROM history")
          self.conn.commit()

     def close(self):
          self.conn.close()