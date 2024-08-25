from abc import ABC, abstractmethod
from datetime import datetime

class Transaction:
    """
    A class to represent a transaction in the bank account.
    """

    def __init__(self, amount: float, transaction_type: str):
        """
        Initialize a Transaction with an amount and a type.
        
        :param amount: The transaction amount.
        :param transaction_type: The type of transaction (e.g., 'Deposit', 'Withdrawal').
        """
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.now()

    def __str__(self) -> str:
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} - {self.transaction_type}: {self.amount:.2f}"

class BankAccount(ABC):
    """
    An abstract base class representing a generic bank account.
    """

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    def get_balance(self) -> float:
        return self.balance

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_transaction_history(self) -> None:
        if not self.transactions:
            print("No transactions found.")
        for transaction in self.transactions:
            print(transaction)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(owner={self.owner}, balance={self.balance:.2f})"

class SavingsAccount(BankAccount):
    """
    A class to represent a savings account.
    """

    def __init__(self, owner: str, balance: float = 0.0, interest_rate: float = 0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.add_transaction(Transaction(amount, 'Deposit'))
        print(f"Deposited {amount:.2f} into Savings Account. New balance: {self.balance:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.add_transaction(Transaction(amount, 'Withdrawal'))
        print(f"Withdrew {amount:.2f} from Savings Account. New balance: {self.balance:.2f}")

    def apply_interest(self) -> None:
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"Applied interest: {interest:.2f}. New balance: {self.balance:.2f}")

class CheckingAccount(BankAccount):
    """
    A class to represent a checking account.
    """

    def __init__(self, owner: str, balance: float = 0.0, overdraft_limit: float = -500.0):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.add_transaction(Transaction(amount, 'Deposit'))
        print(f"Deposited {amount:.2f} into Checking Account. New balance: {self.balance:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < self.overdraft_limit:
            raise ValueError("Overdraft limit reached.")
        self.balance -= amount
        self.add_transaction(Transaction(amount, 'Withdrawal'))
        print(f"Withdrew {amount:.2f} from Checking Account. New balance: {self.balance:.2f}")

def main():
    print("Welcome to the Advanced Bank Account System")
    accounts = {}

    while True:
        print("\nMenu:")
        print("1. Create Savings Account")
        print("2. Create Checking Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. View Balance")
        print("6. View Transaction History")
        print("7. Apply Interest (Savings Account only)")
        print("8. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            owner = input("Enter the account owner's name: ")
            balance = float(input("Enter the initial balance: "))
            account = SavingsAccount(owner, balance)
            accounts[owner] = account
            print(f"Savings account created for {owner}.")
        
        elif choice == '2':
            owner = input("Enter the account owner's name: ")
            balance = float(input("Enter the initial balance: "))
            account = CheckingAccount(owner, balance)
            accounts[owner] = account
            print(f"Checking account created for {owner}.")
        
        elif choice == '3':
            owner = input("Enter the account owner's name: ")
            if owner in accounts:
                amount = float(input("Enter the amount to deposit: "))
                accounts[owner].deposit(amount)
            else:
                print("Account not found.")
        
        elif choice == '4':
            owner = input("Enter the account owner's name: ")
            if owner in accounts:
                amount = float(input("Enter the amount to withdraw: "))
                accounts[owner].withdraw(amount)
            else:
                print("Account not found.")
        
        elif choice == '5':
            owner = input("Enter the account owner's name: ")
            if owner in accounts:
                print(f"Balance: {accounts[owner].get_balance():.2f}")
            else:
                print("Account not found.")
        
        elif choice == '6':
            owner = input("Enter the account owner's name: ")
            if owner in accounts:
                accounts[owner].get_transaction_history()
            else:
                print("Account not found.")
        
        elif choice == '7':
            owner = input("Enter the account owner's name: ")
            if owner in accounts and isinstance(accounts[owner], SavingsAccount):
                accounts[owner].apply_interest()
            else:
                print("Savings account not found.")
        
        elif choice == '8':
            print("Exiting the Advanced Bank Account System.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()