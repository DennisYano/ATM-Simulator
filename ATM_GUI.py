from tkinter import simpledialog
import tkinter as tk
from tkinter import messagebox
import os

DATA_FILE = "accounts.txt"

class Account:
    def __init__(self, name, pin, balance=0.0):
        self.name = name
        self.pin = pin
        self.balance = float(balance)
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount:.2f}")
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount:.2f}")
        else:
            raise ValueError("Insufficient funds.")

    def check_balance(self):
        return self.balance

    def show_transactions(self):
        return self.transactions[-5:]

def load_accounts():
    accounts = {}
    if not os.path.exists(DATA_FILE):
        return accounts
    with open(DATA_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                name, pin, balance = parts[:3]
                accounts[pin] = Account(name, pin, float(balance))
    return accounts

def save_accounts(accounts):
    with open(DATA_FILE, "w") as f:
        for acc in accounts.values():
            f.write(f"{acc.name},{acc.pin},{acc.balance}\n")

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Simulator")
        self.accounts = load_accounts()
        self.current_account = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter PIN:").pack(pady=5)
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        pin = self.pin_entry.get()
        if pin not in self.accounts:
            name = simpledialog.askstring("New Account", "Enter your name:")
            self.accounts[pin] = Account(name, pin)
            messagebox.showinfo("Account Created", "New account created successfully.")
        self.current_account = self.accounts[pin]
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_account.name}", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(fill='x')
        tk.Button(self.root, text="Deposit", command=self.deposit).pack(fill='x')
        tk.Button(self.root, text="Withdraw", command=self.withdraw).pack(fill='x')
        tk.Button(self.root, text="Transaction History", command=self.show_transactions).pack(fill='x')
        tk.Button(self.root, text="Exit", command=self.exit_app).pack(fill='x')

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your balance is ${self.current_account.check_balance():.2f}")

    def deposit(self):
        try:
            amount = float(tk.simpledialog.askstring("Deposit", "Enter amount to deposit:"))
            self.current_account.deposit(amount)
            messagebox.showinfo("Success", "Deposit successful.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = float(tk.simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))
            self.current_account.withdraw(amount)
            messagebox.showinfo("Success", "Withdrawal successful.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_transactions(self):
        transactions = self.current_account.show_transactions()
        if transactions:
            history = "\n".join(transactions)
            messagebox.showinfo("Transaction History", history)
        else:
            messagebox.showinfo("Transaction History", "No transactions yet.")

    def exit_app(self):
        save_accounts(self.accounts)
        self.root.destroy()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
