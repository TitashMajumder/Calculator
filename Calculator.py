import tkinter as tk
import os, sys, re
from math_calculation import safe_eval
from database import get_db_connection, setup_db, save_history

def resource_path(relative_path):
     try:
          base_path = sys._MEIPASS
     except Exception:
          base_path = os.path.abspath(".")
     return os.path.join(base_path, relative_path)

# Initialize App & Database
root = tk.Tk()
conn = get_db_connection()
cursor = conn.cursor()
setup_db(conn)

root.iconbitmap(resource_path("Calculator.ico"))
root.title("Calculator")
root.geometry("340x550")

current_mode = "Rad"
def toggle_mode():
     global current_mode 
     if current_mode == "Rad":
          current_mode = "Deg"
          mode_btn.config(text="DEG", bg="lightblue")
     else:
          current_mode = "Rad"
          mode_btn.config(text="RAD", bg="lightgrey")

# --- UI Functions ---
def press(value):
     if value == "√":
          display.insert(tk.END, "√")
     elif value in ['sin', 'cos', 'tan', 'log', 'ln']:
          display.insert(tk.END, f"{value}(")
     else:
          display.insert(tk.END, value)

def clear_display():
     display.delete(0, tk.END)

def calculate():
     try:
          expression = display.get()

          open_count = expression.count('(')
          close_count = expression.count(')')
          if open_count > close_count:
               expression += ')' * (open_count - close_count)

          eval_expr = expression.replace("√", "sqrt")
          eval_expr = eval_expr.replace("^", "**")
          eval_expr = eval_expr.replace("π", "pi")
          eval_expr = eval_expr.replace("mod", " % ")
          eval_expr = re.sub(r'(\d+(\.\d+)?)\s*([\+\-])\s*(\d+(\.\d+)?)%', r'\1\3(\1*\4/100)', eval_expr)
          eval_expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', eval_expr)
          eval_expr = re.sub(r'\|([^|]+)\|', r'abs(\1)', eval_expr)

          if current_mode == "Deg":
               eval_expr = re.sub(r'(sin|cos|tan)\((.*?)\)', r'\1(rad(\2))', eval_expr)
          if "!" in eval_expr:
               eval_expr = re.sub(r'(\d+|\([^)]+\))!', r'factorial(\1)', eval_expr)
          result = safe_eval(eval_expr)

          display.delete(0, tk.END)
          display.insert(tk.END, result)
          save_history(conn, expression, result)
          update_history()
     except Exception as e:
          display.delete(0, tk.END)
          display.insert(tk.END, "Error")
          print(e)

def update_history():
     history_box.delete(0, tk.END)
     cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
     for expr, res in cursor.fetchall():
          history_box.insert(tk.END, f"{expr} = {res}")

def reuse_history(event):
     selection = history_box.curselection()
     if selection:
          selected_text = history_box.get(selection[0])
          expression = selected_text.split("=")[0].strip()
          display.delete(0, tk.END)
          display.insert(tk.END, expression)

def clear_history():
     cursor.execute("DELETE FROM history")
     conn.commit()
     update_history()

def handle_backspace(event = None):
     current = display.get()
     if current:
          display.delete(len(current)-1, tk.END)

display = tk.Entry(
     root,
     font=("Arial", 20),
     width= 15,
     borderwidth=5,
     relief="ridge",
     justify="right"
)
display.pack(fill="x", padx=15, pady=(15, 2), ipady= 10)

button_frame = tk.Frame(root)
button_frame.pack(pady=2)

buttons = [
     ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('sin', 0, 4),
     ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('cos', 1, 4),
     ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), ('tan', 2, 4),
     ('0', 3, 0), ('%', 3, 1), ('^', 3, 2), ('+', 3, 3), ('log', 3, 4),
     ('.', 4, 0), ('√', 4, 1), ('(', 4, 2), (')', 4, 3), ('ln', 4, 4),
     ('π', 5, 0), ('e', 5, 1), ('!', 5, 2), ('|', 5, 3), ('mod', 5, 4)
]

for (text, row, col) in buttons:
     if text == "":
          continue
     btn = tk.Button(
          button_frame,
          text=text,
          width=4,
          height=1,
          font=("Arial", 15),
          command=lambda t=text: press(t)
     ).grid(row=row, column=col, padx=5, pady=2)

tk.Button(
     button_frame,
     text="⌫",
     width=4,
     height=1,
     font=("Arial", 15),
     command=lambda: handle_backspace(None)
).grid(row=7, column=0, padx=3, pady=3)

tk.Button(
     button_frame,
     text="CLR",
     width=4,
     height=1,
     font=("Arial",15),
     command=clear_display
).grid(row=7, column=1, sticky="we", padx=3, pady=3)

mode_btn = tk.Button(
     button_frame, 
     text="RAD", 
     width=4,
     height=1,
     font=("Arial", 15),
     bg="lightgrey",
     command=toggle_mode,
)
mode_btn.grid(row=7, column=2, sticky="we", padx=3, pady=3)

tk.Button(
     button_frame,
     text="=",
     width=4,
     height=1,
     font=("Arial", 15),
     bg="lightgreen",
     command=calculate
).grid(row=7, column=3, columnspan=2, sticky="we", padx=3, pady=3)

tk.Button(
     root,
     text="Clear History",
     font=("Arial", 10),
     fg="black",
     command=clear_history
).pack(pady=5)

history_frame = tk.Frame(root)
history_frame.pack(fill="both", padx=10, pady=5)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side="right", fill="y")

history_box=tk.Listbox(
     history_frame,
     height=5,
     font=("Arial", 10),
     yscrollcommand=scrollbar.set
)
history_box.pack(side="left", fill="both", expand=True)
scrollbar.config(command=history_box.yview)
history_box.bind("<<ListboxSelect>>", reuse_history)

root.bind('<Return>', lambda e: calculate())
root.bind('<Delete>', lambda e: clear_display())
root.bind('<BackSpace>', handle_backspace)
update_history()
try:
     root.mainloop()
finally:
     conn.close()