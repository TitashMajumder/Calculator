import os, sys, re
import tkinter as tk
from utils import resource_path
from database import DatabaseManager
from math_calculation import ExpressionEval

# Initialize App & Database
class CalculatorApp:
     def __init__(self):
          self.root = tk.Tk()
          self.db = DatabaseManager()
          self.evaluator = ExpressionEval()
          self.current_mode = "Rad"
          self.setup_window()
          self.create_widgets()

     def setup_window(self):
          self.root.title("Calculator")
          self.root.geometry("340x550")
          try:
               self.root.iconbitmap(resource_path("Calculator.ico"))
          except:
               pass

     def toggle_mode(self):
          if self.current_mode == "Rad":
               self.current_mode = "Deg"
               self.mode_btn.config(text="DEG", bg="lightblue")
          else:
               self.current_mode = "Rad"
               self.mode_btn.config(text="RAD", bg="lightgrey")

     # --- UI Functions ---
     def press(self, value):
          if value == "√":
               self.display.insert(tk.END, "√")
          elif value in ['sin', 'cos', 'tan', 'log', 'ln']:
               self.display.insert(tk.END, f"{value}(")
          else:
               self.display.insert(tk.END, value)

     def clear_display(self, event=None):
          self.display.delete(0, tk.END)

     def calculate(self, event=None):
          try:
               expression = self.display.get()
               # 1. Handle Parentheses
               open_count = expression.count('(')
               close_count = expression.count(')')
               if open_count > close_count:
                    expression += ')' * (open_count - close_count)
               # 2. String Pre-processing
               eval_expr = expression.replace("√", "sqrt")
               eval_expr = eval_expr.replace("^", "**")
               eval_expr = eval_expr.replace("π", "pi")
               eval_expr = eval_expr.replace("mod", " % ")
               # 2.1 Percentage Logic
               eval_expr = re.sub(r'(\d+(\.\d+)?)\s*([\+\-])\s*(\d+(\.\d+)?)%', r'\1\3(\1*\4/100)', eval_expr)
               eval_expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', eval_expr)
               eval_expr = re.sub(r'\|([^|]+)\|', r'abs(\1)', eval_expr)
               # 2.2 Trig Mode Logic
               if self.current_mode == "Deg":
                    eval_expr = re.sub(r'(sin|cos|tan)\((.*?)\)', r'\1(rad(\2))', eval_expr)
               # 2.3 Factorial Logic
               if "!" in eval_expr:
                    eval_expr = re.sub(r'(\d+|\([^)]+\))!', r'factorial(\1)', eval_expr)
               # 3. Evaluate using the math engine
               result = self.evaluator.safe_eval(eval_expr)
               self.display.delete(0, tk.END)
               self.display.insert(tk.END, result)
               # 4. Database Save
               self.db.save(expression, result)
               self.update_history()
          except Exception as e:
               self.display.delete(0, tk.END)
               self.display.insert(tk.END, "Error")

     def create_widgets(self):
          # Entry Display
          self.display = tk.Entry(self.root, font=("Arial", 20), width= 15, 
                                  borderwidth=5, relief="ridge", justify="right")
          self.display.pack(fill="x", padx=15, pady=(15, 2), ipady= 10)
          # Button Frame
          button_frame = tk.Frame(self.root)
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
               tk.Button(button_frame, text=text, width=4, height=1, font=("Arial", 15),
                         command=lambda t=text: self.press(t)).grid(row=row, column=col, padx=5, pady=2)

          # Bottom Row Utilities
          tk.Button(button_frame, text="⌫", width=4, height=1, font=("Arial", 15),
                    command=self.handle_backspace).grid(row=7, column=0, padx=3, pady=3)

          tk.Button(button_frame, text="CLR", width=4, height=1, font=("Arial",15), 
                    command=self.clear_display).grid(row=7, column=1, sticky="we", padx=3, pady=3)

          self.mode_btn = tk.Button(button_frame, text="RAD", width=4, height=1, font=("Arial", 15), bg="lightgrey",
                    command=self.toggle_mode)
          self.mode_btn.grid(row=7, column=2, sticky="we", padx=3, pady=3)

          tk.Button(button_frame, text="=", width=4, height=1, font=("Arial", 15), bg="lightgreen",
                   command=self.calculate ).grid(row=7, column=3, columnspan=2, sticky="we", padx=3, pady=3)

          # History Section
          tk.Button(self.root, text="Clear History", font=("Arial", 10), fg="black",
                    command=self.clear_history).pack(pady=5)

          history_frame = tk.Frame(self.root)
          history_frame.pack(fill="both", padx=10, pady=5)

          scrollbar = tk.Scrollbar(history_frame)
          scrollbar.pack(side="right", fill="y")

          self.history_box=tk.Listbox(
               history_frame,
               height=5,
               font=("Arial", 10),
               yscrollcommand=scrollbar.set
          )
          self.history_box.pack(side="left", fill="both", expand=True)
          scrollbar.config(command=self.history_box.yview)
          self.history_box.bind("<<ListboxSelect>>", self.reuse_history)

          self.root.bind('<Return>', lambda e: self.calculate())
          self.root.bind('<Delete>', lambda e: self.clear_display())
          self.root.bind('<BackSpace>', self.handle_backspace)
          self.update_history()

     def update_history(self):
          self.history_box.delete(0, tk.END)
          for expr, res in self.db.fetch_all():
               self.history_box.insert(tk.END, f"{expr} = {res}")

     def reuse_history(self, event):
          selection = self.history_box.curselection()
          if selection:
               selected_text = self.history_box.get(selection[0])
               expression = selected_text.split("=")[0].strip()
               self.display.delete(0, tk.END)
               self.display.insert(tk.END, expression)

     def clear_history(self):
          self.db.clear()
          self.update_history()

     def handle_backspace(self, event=None):
          current = self.display.get()
          if current:
               self.display.delete(len(current)-1, tk.END)

     def run(self):
          try:
               self.root.mainloop()
          finally:
               self.db.close()

# To start the app:
if __name__ == "__main__":
     app = CalculatorApp()
     app.run()