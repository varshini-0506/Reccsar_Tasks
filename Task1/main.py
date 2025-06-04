import tkinter as tk
from tkinter import messagebox, ttk
import math
import sympy as sp

x = sp.symbols('x')  # Declare symbol globally for calculus

def perform_operation(op):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        if op == 'add':
            result = num1 + num2
        elif op == 'sub':
            result = num1 - num2
        elif op == 'mul':
            result = num1 * num2
        elif op == 'div':
            if num2 == 0:
                messagebox.showerror("Math Error", "Cannot divide by zero!")
                return
            result = num1 / num2

        result_label.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")

def evaluate_expression():
    expr = equation_entry.get().strip()
    try:
        if '=' in expr:
            lhs, rhs = expr.split('=')
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation, x)
            result_label.config(text=f"Solved: x = {solution}")
        else:
            safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
            result = eval(expr, {"__builtins__": None}, safe_dict)
            result_label.config(text=f"Evaluated: {result}")
    except Exception as e:
        messagebox.showerror("Expression Error", f"Invalid expression!\n{e}")
        result_label.config(text="")

def perform_calculus(op):
    expr = calculus_entry.get().strip()
    try:
        parsed_expr = sp.sympify(expr)
        if op == 'diff':
            result = sp.diff(parsed_expr, x)
        elif op == 'integrate':
            result = sp.integrate(parsed_expr, x)
        elif op == 'limit':
            result = sp.limit(parsed_expr, x, 0)  # Limit as x→0 (can modify)
        result_label.config(text=f"{op.capitalize()}: {result}")
    except Exception as e:
        messagebox.showerror("Calculus Error", f"Invalid calculus input!\n{e}")
        result_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("Math Toolkit with Calculus")
root.geometry("500x600")
root.configure(bg="#f5f7fa")

# Custom style
style = ttk.Style()
style.theme_use('clam')

# Configure styles
style.configure("TFrame", background="#f5f7fa")
style.configure("TLabel", font=("Segoe UI", 11), background="#f5f7fa", foreground="#2d3436")
style.configure("TButton", font=("Segoe UI", 10), padding=8, relief="flat", 
                background="#3498db", foreground="white")
style.map("TButton", 
          background=[('active', '#2980b9'), ('pressed', '#2c3e50')],
          foreground=[('active', 'white'), ('pressed', 'white')])
style.configure("TLabelFrame", font=("Segoe UI", 12, "bold"), 
               background="#f5f7fa", foreground="#2d3436", borderwidth=2)
style.configure("TEntry", font=("Segoe UI", 11), padding=5, relief="flat")

# Title
title_frame = ttk.Frame(root)
title_frame.pack(pady=(10, 5))
title = tk.Label(title_frame, text="🧮 Advanced Math Toolkit", 
                font=("Segoe UI", 18, "bold"), 
                bg="#f5f7fa", fg="#3498db")
title.pack()

# --- Frame for Basic Operations ---
frame1 = ttk.LabelFrame(root, text="Basic Operations", padding=(15, 10))
frame1.pack(padx=20, pady=10, fill="x")

ttk.Label(frame1, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry1 = ttk.Entry(frame1, style="TEntry")
entry1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame1, text="Number 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry2 = ttk.Entry(frame1, style="TEntry")
entry2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

button_frame = ttk.Frame(frame1)
button_frame.grid(row=2, column=0, columnspan=2, pady=5)

ttk.Button(button_frame, text="➕ Add", command=lambda: perform_operation('add')).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="➖ Subtract", command=lambda: perform_operation('sub')).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="✖ Multiply", command=lambda: perform_operation('mul')).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="➗ Divide", command=lambda: perform_operation('div')).grid(row=1, column=1, padx=5, pady=5)

# --- Frame for Expression Evaluation ---
frame2 = ttk.LabelFrame(root, text="Expression Solver", padding=(15, 10))
frame2.pack(padx=20, pady=10, fill="x")

equation_entry = ttk.Entry(frame2, style="TEntry")
equation_entry.pack(padx=10, pady=10, fill="x")

ttk.Button(frame2, text="🔍 Evaluate / Solve", command=evaluate_expression).pack(pady=5)

# --- Frame for Calculus ---
frame3 = ttk.LabelFrame(root, text="Calculus (using 'x' as variable)", padding=(15, 10))
frame3.pack(padx=20, pady=10, fill="x")

calculus_entry = ttk.Entry(frame3, style="TEntry")
calculus_entry.pack(padx=10, pady=10, fill="x")

calc_button_frame = ttk.Frame(frame3)
calc_button_frame.pack(pady=5)

ttk.Button(calc_button_frame, text="Differentiate", command=lambda: perform_calculus('diff')).grid(row=0, column=0, padx=5)
ttk.Button(calc_button_frame, text="Integrate", command=lambda: perform_calculus('integrate')).grid(row=0, column=1, padx=5)
ttk.Button(calc_button_frame, text="Limit (x→0)", command=lambda: perform_calculus('limit')).grid(row=0, column=2, padx=5)

# --- Result Label ---
result_frame = ttk.Frame(root)
result_frame.pack(pady=15, fill="x")

result_label = tk.Label(result_frame, text="Result will appear here", 
                       font=("Segoe UI", 12, "bold"), 
                       fg="#27ae60", bg="#f5f7fa",
                       wraplength=450, justify="center")
result_label.pack()

# Footer
footer = ttk.Label(root, text="Math Toolkit v1.0", font=("Segoe UI", 8), foreground="#7f8c8d")
footer.pack(side="bottom", pady=5)

root.mainloop()