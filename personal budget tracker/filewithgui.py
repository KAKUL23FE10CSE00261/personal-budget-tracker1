import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# File to store the data
BUDGET_FILE = 'budget_data.csv'

# Function to read data from CSV
def read_data():
    try:
        with open(BUDGET_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

# Function to write data to CSV
def write_data(data):
    with open(BUDGET_FILE, 'w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'type']  # Type is income or expense
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to add a new entry
def add_entry(entry_type, category, amount):
    data = read_data()
    
    if not category or not amount:
        messagebox.showerror("Error", "Category and Amount are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a number.")
        return

    entry = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'category': category,
        'amount': amount,
        'type': entry_type
    }

    data.append(entry)
    write_data(data)
    messagebox.showinfo("Success", "Entry added successfully!")

# Function to show the budget summary
def show_summary():
    data = read_data()

    total_income = sum(float(entry['amount']) for entry in data if entry['type'] == 'income')
    total_expenses = sum(float(entry['amount']) for entry in data if entry['type'] == 'expense')
    balance = total_income - total_expenses

    summary = (
        f"Total Income: ${total_income:.2f}\n"
        f"Total Expenses: ${total_expenses:.2f}\n"
        f"Balance: ${balance:.2f}"
    )
    messagebox.showinfo("Budget Summary", summary)

# Function to show expenses by category
def show_expenses_by_category():
    data = read_data()
    categories = {}

    for entry in data:
        if entry['type'] == 'expense':
            category = entry['category']
            amount = float(entry['amount'])
            categories[category] = categories.get(category, 0) + amount

    if not categories:
        messagebox.showinfo("Expenses by Category", "No expenses recorded yet.")
        return

    result = "\n".join(f"{category.capitalize()}: ${total:.2f}" for category, total in categories.items())
    messagebox.showinfo("Expenses by Category", result)

# GUI Setup
def main():
    root = tk.Tk()
    root.title("Personal Budget Tracker")
    root.geometry("400x400")

    # Add Entry Frame
    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
    category_entry = tk.Entry(frame, width=20)
    category_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(frame, width=20)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Type:").grid(row=2, column=0, padx=5, pady=5)
    entry_type = ttk.Combobox(frame, values=["income", "expense"], state="readonly")
    entry_type.grid(row=2, column=1, padx=5, pady=5)

    def add_button_action():
        add_entry(entry_type.get(), category_entry.get(), amount_entry.get())
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

    add_button = tk.Button(frame, text="Add Entry", command=add_button_action)
    add_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Buttons for Summary and Expenses by Category
    summary_button = tk.Button(root, text="View Budget Summary", command=show_summary)
    summary_button.pack(pady=10)

    category_button = tk.Button(root, text="View Expenses by Category", command=show_expenses_by_category)
    category_button.pack(pady=10)

    # Exit Button
    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
