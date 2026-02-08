import tkinter as tk
import ast
import operator
import sqlite3
import os, sys

def resource_path(relative_path):
     try:
          base_path = sys._MEIPASS
     except Exception:
          base_path = os.path.abspath(".")
     return os.path.join(base_path, relative_path)

root = tk.Tk()
root.iconbitmap(resource_path("Cal.ico"))
root.title("Calculator")
root.geometry("310x560")
history = []

def get_app_data_path():
     app_name = "CalculatorApp"
     base_dir = os.getenv("LOCALAPPDATA")
     app_dir = os.path.join(base_dir, app_name)
     if not os.path.exists(app_dir):
          os.makedirs(app_dir)
     return app_dir

db_path = os.path.join(get_app_data_path(), "calculator_history.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS history(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               expression TEXT NOT NULL,
               result TEXT NOT NULL)
               """)
conn.commit()

display = tk.Entry(
     root,
     font=("Arial", 20),
     borderwidth=5,
     relief="ridge",
     justify="right"
)

ALLOWED_OPERATORS = {
     ast.Add: operator.add,
     ast.Sub: operator.sub,
     ast.Mult: operator.mul,
     ast.Div: operator.truediv,
     ast.Mod: operator.mod,
}

display.pack(fill="x", padx=10, pady=10)

def press(value):
     display.insert(tk.END, value)

def clear_display():
     display.delete(0, tk.END)

def safe_eval(expr):
     def _eval(node):
          if isinstance(node, ast.Expression):
               return _eval(node.body)
          elif isinstance(node, ast.BinOp):
               left = _eval(node.left)
               right = _eval(node.right)
               op_type = type(node.op)
               if op_type in ALLOWED_OPERATORS:
                    return ALLOWED_OPERATORS[op_type](left, right)
               else:
                    raise ValueError("Unsupported operator")
          elif isinstance(node, ast.Num):
               return node.n
          elif isinstance(node, ast.Constant):
               if isinstance(node.value, (int, float)):
                    return node.value
               else:
                    raise ValueError("Invalid constant")
          else:
               raise ValueError("Invalid expression")
     tree = ast.parse(expr, mode='eval')
     return _eval(tree)

def calculate():
     try:
          expression = display.get()
          result = safe_eval(expression)
          display.delete(0, tk.END)
          display.insert(tk.END, result)
          entry = f"{expression} = {result}"
          cursor.execute(
                    "INSERT INTO history (expression, result) VALUES (?, ?)",
                    (expression, str(result))
          )
          conn.commit()
          cursor.execute("""
          DELETE FROM history
          WHERE id NOT IN(
          SELECT id FROM history
          ORDER BY id DESC
          LIMIT 20)""")
          conn.commit()
          update_history()
     except:
          display.delete(0, tk.END)
          display.insert(tk.END, "Error")

def update_history():
     history_box.delete(0, tk.END)
     cursor.execute("""
          SELECT expression, result
          FROM history
          ORDER BY id DESC
     """)
     rows = cursor.fetchall()
     for expr, res in rows:
          history_box.insert(tk.END, f"{expr} = {res}")

def reuse_history(event):
     selection = history_box.curselection()
     if not selection:
          return
     selected_text = history_box.get(selection[0])
     expression = selected_text.split("0")[0].strip()
     display.delete(0, tk.END)
     display.insert(tk.END, expression)

button_frame = tk.Frame(root)
button_frame.pack()

buttons = [
     ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('+', 0, 3),
     ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('-', 1, 3),
     ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('*', 2, 3),
     ('0', 3, 0), ('00', 3, 1), ('%', 3, 2), ('/', 3, 3),
]

for (text, row, col) in buttons:
     if text == "":
          continue
     btn = tk.Button(
          button_frame,
          text=text,
          width=5,
          height=2,
          font=("Arial", 15),
          command=lambda t=text: press(t)
     ).grid(row=row, column=col, padx=5, pady=5)

tk.Button(
     button_frame,
     text="CLEAR",
     height=2,
     font=("Arial",15),
     command=clear_display
).grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)

tk.Button(
     button_frame,
     text="=",
     height=2,
     font=("Arial", 15),
     bg="lightgreen",
     command=calculate
).grid(row=4, column=2, columnspan=2, sticky="we", padx=5, pady=5)

history_label=tk.Label(
     root,
     text="History (Last 20)",
     font=("Arial", 12, "bold")
)
history_label.pack(pady=(10, 0))

history_box=tk.Listbox(
     root,
     height=5,
     font=("Arial", 10)
)
history_box.pack(fill="both", padx=10, pady=5)
history_box.bind("<<ListboxSelect>>", reuse_history)

update_history()
root.mainloop()