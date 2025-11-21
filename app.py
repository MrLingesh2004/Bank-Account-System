import json
import os
import time
import random

# -------------------------
# Colored output
# -------------------------
class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# -------------------------
# Bank System Class
# -------------------------
class BankSystem:
    def __init__(self, file="bank_data.json"):
        self.file = file
        self.accounts = {}
        self.load_accounts()
        self.admin_password = "admin123"  # Admin password

    # -------------------------
    # File Operations
    # -------------------------
    def load_accounts(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    self.accounts = json.load(f)
            except:
                self.accounts = {}
        else:
            self.accounts = {}

    def save_accounts(self):
        with open(self.file, "w") as f:
            json.dump(self.accounts, f, indent=4)

    # -------------------------
    # Helper Methods
    # -------------------------
    def account_exists(self, name):
        return name in self.accounts

    def validate_pin(self, name, pin):
        return self.accounts[name]["pin"] == pin

    def generate_acc_number(self):
        while True:
            acc_no = str(random.randint(10000000, 99999999))
            if not any(acc["account_no"] == acc_no for acc in self.accounts.values()):
                return acc_no

    # -------------------------
    # Account CRUD
    # -------------------------
    def create_account(self, name, pin, acc_type="normal"):
        if self.account_exists(name):
            print(f"{Color.YELLOW}Account already exists!{Color.RESET}")
            return

        acc_no = self.generate_acc_number()
        self.accounts[name] = {
            "pin": pin,
            "balance": 0,
            "history": [],
            "type": acc_type,
            "interest_rate": 2.5 if acc_type == "savings" else 0,
            "account_no": acc_no
        }
        self.save_accounts()
        print(f"{Color.GREEN}Account created successfully! Account No: {acc_no}{Color.RESET}")

    def deposit(self, name, amount):
        if amount <= 0:
            print(f"{Color.RED}Invalid amount!{Color.RESET}")
            return

        self.accounts[name]["balance"] += amount
        self.accounts[name]["history"].append(f"Deposited ₹{amount}")
        self.save_accounts()
        print(f"{Color.GREEN}Deposited ₹{amount}{Color.RESET}")

    def withdraw(self, name, amount):
        if amount <= 0:
            print(f"{Color.RED}Invalid amount!{Color.RESET}")
            return

        if amount > self.accounts[name]["balance"]:
            print(f"{Color.RED}Insufficient balance!{Color.RESET}")
            return

        self.accounts[name]["balance"] -= amount
        self.accounts[name]["history"].append(f"Withdrew ₹{amount}")
        self.save_accounts()
        print(f"{Color.YELLOW}Withdrew ₹{amount}{Color.RESET}")

    def add_interest(self, name):
        acc = self.accounts[name]
        if acc["type"] != "savings":
            print(f"{Color.RED}Not a savings account!{Color.RESET}")
            return

        interest = acc["balance"] * (acc["interest_rate"] / 100)
        acc["balance"] += interest
        acc["history"].append(f"Interest added ₹{interest:.2f}")
        self.save_accounts()
        print(f"{Color.CYAN}Interest added: ₹{interest:.2f}{Color.RESET}")

    def show_history(self, name):
        history = self.accounts[name]["history"]
        print(f"\n{Color.BOLD}{Color.CYAN}--- Transaction History ---{Color.RESET}")
        if not history:
            print(f"{Color.YELLOW}No transactions found.{Color.RESET}")
        else:
            for h in history:
                print(f"{Color.BLUE}• {h}{Color.RESET}")
        print("")

    def close_account(self, name):
        confirm = input(f"{Color.RED}Are you sure you want to close this account? (y/n): {Color.RESET}")
        if confirm.lower() == "y":
            del self.accounts[name]
            self.save_accounts()
            print(f"{Color.RED}Account closed successfully!{Color.RESET}")
            return True
        return False

    # -------------------------
    # Login System
    # -------------------------
    def login(self):
        name = input("Enter Account Name: ")

        if not self.account_exists(name):
            print(f"{Color.RED}Account not found!{Color.RESET}")
            return None

        pin = input("Enter PIN: ")
        if not self.validate_pin(name, pin):
            print(f"{Color.RED}Incorrect PIN!{Color.RESET}")
            return None

        print(f"{Color.GREEN}Login Successful!{Color.RESET}")
        return name

    # -------------------------
    # Admin Mode
    # -------------------------
    def admin_mode(self):
        pwd = input("Enter Admin Password: ")
        if pwd != self.admin_password:
            print(f"{Color.RED}Incorrect Admin Password!{Color.RESET}")
            return

        print(f"{Color.GREEN}Welcome, Admin!{Color.RESET}")
        while True:
            print(f"""
{Color.BOLD}{Color.CYAN}=========== ADMIN MENU ==========={Color.RESET}
1. View All Accounts
2. Delete Account
3. Exit Admin
{Color.CYAN}================================={Color.RESET}
""")
            choice = input("Choose an option: ")

            if choice == "1":
                if not self.accounts:
                    print(f"{Color.YELLOW}No accounts found.{Color.RESET}")
                else:
                    print(f"{Color.BOLD}{Color.BLUE}--- All Accounts ---{Color.RESET}")
                    for name, acc in self.accounts.items():
                        print(f"{Color.GREEN}Name:{Color.RESET} {name} | {Color.GREEN}Acc No:{Color.RESET} {acc['account_no']} | {Color.GREEN}Type:{Color.RESET} {acc['type'].capitalize()} | {Color.GREEN}Balance:{Color.RESET} ₹{acc['balance']}")
            elif choice == "2":
                target = input("Enter Account Name to delete: ")
                if self.account_exists(target):
                    del self.accounts[target]
                    self.save_accounts()
                    print(f"{Color.RED}Account deleted successfully!{Color.RESET}")
                else:
                    print(f"{Color.RED}Account not found!{Color.RESET}")
            elif choice == "3":
                break
            else:
                print(f"{Color.RED}Invalid option!{Color.RESET}")

    # -------------------------
    # CLI Animation
    # -------------------------
    def loading_animation(self, msg="Processing"):
        for i in range(3):
            print(f"{Color.CYAN}{msg}{'.' * (i+1)}{Color.RESET}", end="\r")
            time.sleep(0.5)
        print(" " * (len(msg)+3), end="\r")  # clear line

    # -------------------------
    # Menus
    # -------------------------
    def show_main_menu(self):
        print(f"""
{Color.BOLD}{Color.BLUE}========== BANK ACCOUNT SYSTEM =========={Color.RESET}
1. Create Account
2. Login to Account
3. Admin Mode
4. Exit
{Color.BLUE}=========================================={Color.RESET}
""")

    def show_user_menu(self, name):
        print(f"""
{Color.BOLD}{Color.CYAN}=========== ACCOUNT MENU ==========={Color.RESET}
Account: {Color.GREEN}{name}{Color.RESET}
Account No: {self.accounts[name]['account_no']}
Type: {self.accounts[name]['type'].capitalize()}
Balance: ₹{self.accounts[name]['balance']}

1. Deposit
2. Withdraw
3. View Balance
4. View History
5. Add Interest (Savings Only)
6. Close Account
7. Logout
{Color.CYAN}====================================={Color.RESET}
""")

    # -------------------------
    # Main App
    # -------------------------
    def main(self):
        print(f"{Color.GREEN}{Color.BOLD}Welcome to the Bank System!{Color.RESET}")

        while True:
            self.show_main_menu()
            choice = input(f"{Color.CYAN}Enter an option: {Color.RESET}")

            if choice == "1":
                name = input("Enter Name: ")
                pin = input("Set PIN: ")
                acc_type = input("Savings Account? (y/n): ")
                acc_type = "savings" if acc_type.lower() == "y" else "normal"
                self.loading_animation("Creating Account")
                self.create_account(name, pin, acc_type)

            elif choice == "2":
                user = self.login()
                if not user:
                    continue

                while True:
                    self.show_user_menu(user)
                    c = input(f"{Color.YELLOW}Choose an option: {Color.RESET}")

                    if c == "1":
                        amt = float(input("Amount: "))
                        self.loading_animation("Depositing")
                        self.deposit(user, amt)
                    elif c == "2":
                        amt = float(input("Amount: "))
                        self.loading_animation("Withdrawing")
                        self.withdraw(user, amt)
                    elif c == "3":
                        print(f"{Color.BLUE}Balance: ₹{self.accounts[user]['balance']}{Color.RESET}")
                    elif c == "4":
                        self.show_history(user)
                    elif c == "5":
                        self.loading_animation("Adding Interest")
                        self.add_interest(user)
                    elif c == "6":
                        closed = self.close_account(user)
                        if closed:
                            break
                    elif c == "7":
                        print(f"{Color.YELLOW}Logged out!{Color.RESET}")
                        break
                    else:
                        print(f"{Color.RED}Invalid Option!{Color.RESET}")

            elif choice == "3":
                self.admin_mode()

            elif choice == "4":
                print(f"{Color.YELLOW}Goodbye!{Color.RESET}")
                break

            else:
                print(f"{Color.RED}Invalid Option!{Color.RESET}")


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    BankSystem().main()