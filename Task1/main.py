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
root.geometry("460x540")
root.configure(bg="#f0f4f8")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 11), padding=5)

title = tk.Label(root, text="🧮 Math Toolkit", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#333")
title.pack(pady=10)

# --- Frame for Basic Operations ---
frame1 = ttk.LabelFrame(root, text="Basic Operations")
frame1.pack(padx=20, pady=10, fill="x")

ttk.Label(frame1, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry1 = ttk.Entry(frame1)
entry1.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame1, text="Number 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry2 = ttk.Entry(frame1)
entry2.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame1, text="Add", command=lambda: perform_operation('add')).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(frame1, text="Subtract", command=lambda: perform_operation('sub')).grid(row=2, column=1, padx=5, pady=5)
ttk.Button(frame1, text="Multiply", command=lambda: perform_operation('mul')).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(frame1, text="Divide", command=lambda: perform_operation('div')).grid(row=3, column=1, padx=5, pady=5)

# --- Frame for Expression Evaluation ---
frame2 = ttk.LabelFrame(root, text="Expression Solver")
frame2.pack(padx=20, pady=10, fill="x")

equation_entry = ttk.Entry(frame2, width=30)
equation_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

ttk.Button(frame2, text="Evaluate / Solve", command=evaluate_expression).grid(row=1, column=0, columnspan=2, pady=5)

# --- Frame for Calculus ---
frame3 = ttk.LabelFrame(root, text="Calculus (using 'x' as variable)")
frame3.pack(padx=20, pady=10, fill="x")

calculus_entry = ttk.Entry(frame3, width=30)
calculus_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

ttk.Button(frame3, text="Differentiate", command=lambda: perform_calculus('diff')).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame3, text="Integrate", command=lambda: perform_calculus('integrate')).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(frame3, text="Limit (x→0)", command=lambda: perform_calculus('limit')).grid(row=1, column=2, padx=5, pady=5)

# --- Result Label ---
result_label = tk.Label(root, text="Result will appear here", font=("Arial", 12), fg="blue", bg="#f0f4f8")
result_label.pack(pady=15)

root.mainloop()
