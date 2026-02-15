## ﻿🧮 Calculator Application (OOP • Tkinter • Python)
A feature-rich scientific calculator built using Python (Tkinter) with a clean Object-Oriented Programming (OOP) architecture.
The application supports advanced mathematical operations, safe expression evaluation, and persistent calculation history using SQLite.

## ✨ Features
- Basic arithmetic operations (+ − × ÷)
- Scientific functions: sin, cos, tan, log, ln, √, !
- Degree / Radian mode toggle
- Percentage calculations
- Absolute value support |x|
- Parentheses handling
- Safe expression evaluation using AST (no eval)
- Calculation history stored locally (SQLite)
- Reuse previous calculations
- Clear history option
- Clean OOP-based design
- Windows executable support (.exe)

## 🧠 Project Architecture (OOP)
```
calculator/
│
├── Calculator.py          # Main Tkinter application (UI layer)
├── math_calculation.py    # Safe AST-based expression evaluator
├── database.py            # SQLite database manager
├── utils.py               # Utility helpers (PyInstaller path handling)
├── Calculator.ico         # Application icon
└── README.md
```
## 🔐 Security Design
- No use of eval()
- Uses Python ast module for safe evaluation
- Only whitelisted operators and functions are allowed
- Prevents arbitrary code execution

## 🖥️ Screens & UI
- Built using Tkinter
- Responsive button layout
- Keyboard support:
  - Enter → Calculate
  - Backspace → Delete last character
  - Delete → Clear input

## 🗃️ Database (SQLite)
- Stores calculation history locally
- Automatically limits history to last 20 calculations
- Stored in:
```
%LOCALAPPDATA%/CalculatorAPP/calculator_history.db
```

## 🚀 Installation & Usage
### ▶️ Run from Source
#### 1️⃣ Clone the repository
```
git clone https://github.com/TitashMajumder/Calculator.git
cd Calculator
```
#### 2️⃣ Run the app
```
python Calculator.py
```
- Python 3.8+ recommended

## 🪟 Windows Executable (.exe)
You can download the standalone Windows executable from the GitHub Releases section.
- No Python installation required
- Built using PyInstaller
- If Windows Defender warns:
Click More Info → Run Anyway

## ⚙️ Build EXE (Optional)
```
pyinstaller --onefile --windowed --icon=Calculator.ico Calculator.py
```
- The executable will be generated inside the dist/ folder.

## 🧪 Technologies Used
- Python 3
- Tkinter (GUI)
- SQLite3 (local storage)
- AST module (secure evaluation)
- PyInstaller (packaging)

## 📌 Why This Project?
#### This project demonstrates:
- Strong OOP principles
- Secure coding practices
- GUI development skills
- Local data persistence
- Production-ready Python application design

## 📄 License
This project is released under the MIT License.
Feel free to use, modify, and distribute.

## 👤 Author
**Titash Majumder**
B.Tech (Information Technology)
Interested in Software Development, AI & Cybersecurity

## ⭐ Support
#### If you like this project:
- ⭐ Star the repository
- 🍴 Fork it
- 🐞 Open issues for suggestions or bugs




