import pandas
import csv
from datetime import datetime

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

# Function to add income or expense
def add_entry():
    data = read_data()
    print("Enter the type of entry (income/expense): ")
    entry_type = input().lower()

    if entry_type not in ['income', 'expense']:
        print("Invalid entry type. Try again.")
        return

    print("Enter the category (e.g., food, entertainment): ")
    category = input().strip()

    print("Enter the amount: ")
    try:
        amount = float(input().strip())
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Add the new entry
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'category': category,
        'amount': amount,
        'type': entry_type
    }

    data.append(entry)
    write_data(data)
    print("Entry added successfully!")

# Function to show budget summary
def show_summary():
    data = read_data()

    total_income = sum(float(entry['amount']) for entry in data if entry['type'] == 'income')
    total_expenses = sum(float(entry['amount']) for entry in data if entry['type'] == 'expense')
    balance = total_income - total_expenses

    print("\nBudget Summary:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Balance: ${balance:.2f}")

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
        print("No expenses recorded yet.")
        return

    print("\nExpenses by Category:")
    for category, total in categories.items():
        print(f"{category.capitalize()}: ${total:.2f}")

# Function to display the menu
def display_menu():
    print("\nPersonal Budget Tracker")
    print("1. Add Income/Expense")
    print("2. View Budget Summary")
    print("3. View Expenses by Category")
    print("4. Exit")

# Main loop to run the application
def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            add_entry()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            show_expenses_by_category()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
