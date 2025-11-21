import json
import os

# Colored output (Same as your ToDoTask app)
class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class BankSystem:
    def __init__(self, file="bank_data.json"):
        self.file = file
        self.accounts = {}
        self.load_accounts()

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
    # Helper
    # -------------------------
    def account_exists(self, name):
        return name in self.accounts

    def validate_pin(self, name, pin):
        return self.accounts[name]["pin"] == pin

    # -------------------------
    # Account CRUD
    # -------------------------
    def create_account(self, name, pin, acc_type="normal"):
        if self.account_exists(name):
            print(f"{Color.YELLOW}Account already exists!{Color.RESET}")
            return

        self.accounts[name] = {
            "pin": pin,
            "balance": 0,
            "history": [],
            "type": acc_type,
            "interest_rate": 2.5 if acc_type == "savings" else 0
        }

        self.save_accounts()
        print(f"{Color.GREEN}Account created successfully!{Color.RESET}")

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

    # -------------------------
    # LOGIN SYSTEM
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
    # Menu UI
    # -------------------------
    def show_menu(self):
        print(f"""
{Color.BOLD}{Color.BLUE}========== BANK ACCOUNT SYSTEM =========={Color.RESET}
1. Create Account
2. Login to Account
3. Exit
{Color.BLUE}=========================================={Color.RESET}
""")

    def show_user_menu(self, name):
        print(f"""
{Color.BOLD}{Color.CYAN}=========== ACCOUNT MENU ==========={Color.RESET}
Account: {Color.GREEN}{name}{Color.RESET}
Type: {self.accounts[name]["type"].capitalize()}
Balance: ₹{self.accounts[name]["balance"]}

1. Deposit
2. Withdraw
3. View Balance
4. View History
5. Add Interest (Savings Only)
6. Logout
{Color.CYAN}====================================={Color.RESET}
""")

    # -------------------------
    # MAIN APP
    # -------------------------
    def main(self):
        print(f"{Color.GREEN}{Color.BOLD}Welcome to the Bank System!{Color.RESET}")

        while True:
            self.show_menu()
            choice = input(f"{Color.CYAN}Enter an option: {Color.RESET}")

            # CREATE ACCOUNT
            if choice == "1":
                name = input("Enter Name: ")
                pin = input("Set PIN: ")
                acc_type = input("Savings Account? (y/n): ")

                acc_type = "savings" if acc_type.lower() == "y" else "normal"
                self.create_account(name, pin, acc_type)

            # LOGIN
            elif choice == "2":
                user = self.login()
                if not user:
                    continue

                # USER LOGGED IN MENU
                while True:
                    self.show_user_menu(user)
                    c = input(f"{Color.YELLOW}Choose an option: {Color.RESET}")

                    if c == "1":
                        amt = float(input("Amount: "))
                        self.deposit(user, amt)

                    elif c == "2":
                        amt = float(input("Amount: "))
                        self.withdraw(user, amt)

                    elif c == "3":
                        print(f"{Color.BLUE}Balance: ₹{self.accounts[user]['balance']}{Color.RESET}")

                    elif c == "4":
                        self.show_history(user)

                    elif c == "5":
                        self.add_interest(user)

                    elif c == "6":
                        print(f"{Color.YELLOW}Logged out!{Color.RESET}")
                        break

                    else:
                        print(f"{Color.RED}Invalid Option!{Color.RESET}")

            # EXIT
            elif choice == "3":
                print(f"{Color.YELLOW}Goodbye!{Color.RESET}")
                break

            else:
                print(f"{Color.RED}Invalid Option! Try again.{Color.RESET}")


if __name__ == '__main__':
    BankSystem().main()