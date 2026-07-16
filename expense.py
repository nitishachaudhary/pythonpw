"""
Expense Tracker
----------------
A simple console-based Personal Expense Tracker built with Python.

Features:
- Add income and expense transactions
- View all transactions
- View category-wise summary
- View monthly summary
- Calculate current balance
- Persistent storage using JSON (no database required)

Author: <Your Name>
Course: BSc CSIT
"""

import json
import os
from datetime import datetime

DATA_FILE = "transactions.json"


# ---------------------------------------------------------------------
# Data persistence helpers
# ---------------------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------------------
# Core class
# ---------------------------------------------------------------------
class ExpenseTracker:
    def __init__(self):
        self.transactions = load_data()

    def add_transaction(self, t_type, category, amount, note=""):
        transaction = {
            "id": len(self.transactions) + 1,
            "type": t_type,          # "income" or "expense"
            "category": category,
            "amount": amount,
            "note": note,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        self.transactions.append(transaction)
        save_data(self.transactions)
        print(f"{t_type.capitalize()} of {amount} added under '{category}'.")

    def view_all(self):
        if not self.transactions:
            print("No transactions recorded yet.")
            return
        print(f"{'ID':<5}{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':<10}{'Note'}")
        print("-" * 70)
        for t in self.transactions:
            print(f"{t['id']:<5}{t['date']:<12}{t['type']:<10}"
                  f"{t['category']:<15}{t['amount']:<10}{t['note']}")

    def delete_transaction(self, t_id):
        original_len = len(self.transactions)
        self.transactions = [t for t in self.transactions if t["id"] != t_id]
        if len(self.transactions) == original_len:
            print("Transaction ID not found.")
        else:
            save_data(self.transactions)
            print("Transaction deleted.")

    def get_balance(self):
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return income, expense, income - expense

    def category_summary(self):
        summary = {}
        for t in self.transactions:
            if t["type"] == "expense":
                summary[t["category"]] = summary.get(t["category"], 0) + t["amount"]

        if not summary:
            print("No expenses recorded yet.")
            return

        print(f"{'Category':<20}{'Total Spent'}")
        print("-" * 35)
        for cat, total in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"{cat:<20}{total}")

    def monthly_summary(self):
        summary = {}
        for t in self.transactions:
            month = t["date"][:7]  # YYYY-MM
            summary.setdefault(month, {"income": 0, "expense": 0})
            summary[month][t["type"]] += t["amount"]

        if not summary:
            print("No transactions recorded yet.")
            return

        print(f"{'Month':<10}{'Income':<12}{'Expense':<12}{'Net'}")
        print("-" * 45)
        for month, values in sorted(summary.items()):
            net = values["income"] - values["expense"]
            print(f"{month:<10}{values['income']:<12}{values['expense']:<12}{net}")


# ---------------------------------------------------------------------
# Console menu
# ---------------------------------------------------------------------
def main():
    tracker = ExpenseTracker()

    menu = """
=========== EXPENSE TRACKER ===========
1. Add Income
2. Add Expense
3. View All Transactions
4. Delete Transaction
5. View Balance
6. Category-wise Summary
7. Monthly Summary
8. Exit
=========================================
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            category = input("Income source (e.g. Salary, Gift): ").strip()
            amount = float(input("Amount: ").strip())
            note = input("Note (optional): ").strip()
            tracker.add_transaction("income", category, amount, note)

        elif choice == "2":
            category = input("Expense category (e.g. Food, Transport): ").strip()
            amount = float(input("Amount: ").strip())
            note = input("Note (optional): ").strip()
            tracker.add_transaction("expense", category, amount, note)

        elif choice == "3":
            tracker.view_all()

        elif choice == "4":
            t_id = int(input("Enter transaction ID to delete: ").strip())
            tracker.delete_transaction(t_id)

        elif choice == "5":
            income, expense, balance = tracker.get_balance()
            print(f"\nTotal Income:  {income}")
            print(f"Total Expense: {expense}")
            print(f"Current Balance: {balance}")

        elif choice == "6":
            tracker.category_summary()

        elif choice == "7":
            tracker.monthly_summary()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()