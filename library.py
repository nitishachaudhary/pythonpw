"""
Library Management System
--------------------------
A simple console-based Library Management System built with Python.

Features:
- Add, view, search, update, and delete books
- Register library members
- Issue and return books
- Persistent storage using JSON (no database required)
- Basic fine calculation for overdue books

Author: <Your Name>
Course: BSc CSIT
"""

import json
import os
from datetime import datetime, timedelta

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"
FINE_PER_DAY = 5          # currency units per day overdue
LOAN_PERIOD_DAYS = 14     # standard borrowing period


# ---------------------------------------------------------------------
# Data persistence helpers
# ---------------------------------------------------------------------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4, default=str)


# ---------------------------------------------------------------------
# Core class
# ---------------------------------------------------------------------
class Library:
    def __init__(self):
        self.books = load_data(BOOKS_FILE)      # key: book_id
        self.members = load_data(MEMBERS_FILE)  # key: member_id

    # ---------------- Book management ----------------
    def add_book(self, book_id, title, author, copies):
        if book_id in self.books:
            print("Book ID already exists.")
            return
        self.books[book_id] = {
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
        }
        save_data(BOOKS_FILE, self.books)
        print(f"Book '{title}' added successfully.")

    def view_books(self):
        if not self.books:
            print("No books in the library.")
            return
        print(f"{'ID':<8}{'Title':<25}{'Author':<20}{'Available':<10}{'Total'}")
        print("-" * 70)
        for bid, b in self.books.items():
            print(f"{bid:<8}{b['title']:<25}{b['author']:<20}"
                  f"{b['available_copies']:<10}{b['total_copies']}")

    def search_book(self, keyword):
        keyword = keyword.lower()
        results = {
            bid: b for bid, b in self.books.items()
            if keyword in b["title"].lower() or keyword in b["author"].lower()
        }
        if not results:
            print("No matching books found.")
        else:
            for bid, b in results.items():
                print(f"{bid} -> {b['title']} by {b['author']} "
                      f"(Available: {b['available_copies']}/{b['total_copies']})")

    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            save_data(BOOKS_FILE, self.books)
            print("Book deleted.")
        else:
            print("Book ID not found.")

    # ---------------- Member management ----------------
    def add_member(self, member_id, name):
        if member_id in self.members:
            print("Member ID already exists.")
            return
        self.members[member_id] = {"name": name, "borrowed_books": {}}
        save_data(MEMBERS_FILE, self.members)
        print(f"Member '{name}' registered successfully.")

    def view_members(self):
        if not self.members:
            print("No registered members.")
            return
        for mid, m in self.members.items():
            print(f"{mid} -> {m['name']} | Borrowed: {list(m['borrowed_books'].keys())}")

    # ---------------- Issue / Return ----------------
    def issue_book(self, member_id, book_id):
        if member_id not in self.members:
            print("Member not found.")
            return
        if book_id not in self.books:
            print("Book not found.")
            return
        if self.books[book_id]["available_copies"] <= 0:
            print("No copies available right now.")
            return

        due_date = (datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)).strftime("%Y-%m-%d")
        self.members[member_id]["borrowed_books"][book_id] = due_date
        self.books[book_id]["available_copies"] -= 1

        save_data(BOOKS_FILE, self.books)
        save_data(MEMBERS_FILE, self.members)
        print(f"Book issued. Due date: {due_date}")

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            print("Member not found.")
            return
        borrowed = self.members[member_id]["borrowed_books"]
        if book_id not in borrowed:
            print("This member did not borrow this book.")
            return

        due_date = datetime.strptime(borrowed[book_id], "%Y-%m-%d")
        overdue_days = (datetime.now() - due_date).days
        fine = max(0, overdue_days) * FINE_PER_DAY

        del borrowed[book_id]
        self.books[book_id]["available_copies"] += 1

        save_data(BOOKS_FILE, self.books)
        save_data(MEMBERS_FILE, self.members)

        if fine > 0:
            print(f"Book returned. Overdue by {overdue_days} days. Fine: {fine}")
        else:
            print("Book returned on time. No fine.")


# ---------------------------------------------------------------------
# Console menu
# ---------------------------------------------------------------------
def main():
    lib = Library()

    menu = """
========== LIBRARY MANAGEMENT SYSTEM ==========
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
5. Register Member
6. View Members
7. Issue Book
8. Return Book
9. Exit
=================================================
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            bid = input("Book ID: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            copies = int(input("Number of copies: ").strip())
            lib.add_book(bid, title, author, copies)

        elif choice == "2":
            lib.view_books()

        elif choice == "3":
            keyword = input("Enter title/author keyword: ").strip()
            lib.search_book(keyword)

        elif choice == "4":
            bid = input("Book ID to delete: ").strip()
            lib.delete_book(bid)

        elif choice == "5":
            mid = input("Member ID: ").strip()
            name = input("Member name: ").strip()
            lib.add_member(mid, name)

        elif choice == "6":
            lib.view_members()

        elif choice == "7":
            mid = input("Member ID: ").strip()
            bid = input("Book ID: ").strip()
            lib.issue_book(mid, bid)

        elif choice == "8":
            mid = input("Member ID: ").strip()
            bid = input("Book ID: ").strip()
            lib.return_book(mid, bid)

        elif choice == "9":
            print("Goodbye!")
            break