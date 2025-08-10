from typing import List, Dict
from datetime import datetime
from src.transaction import Transaction
class Account:
    """
    This class represents generic bank account
    """
    def __init__(self, account_name: str, account_type: str,initial_balance: float = 0.0):
        """
      Initializes an Account object.

      Args:
          account_name (str): The name of the account.
          account_type (str): The type of the account (e.g., 'Checking', 'Savings').
          initial_balance (float): The starting balance of the account.
      """
        self.account_name = account_name
        self.account_type = account_type
        self._balance = initial_balance  # protected attribute for balance
        self.transaction_list: List[Transaction] = []

    def add_transaction(self, transaction:Transaction):
        self.transaction_list.append(transaction)
        self._balance += transaction.amount
        print(f"Transaction added. New balance: ${self._balance:.2f}")

    def remove_transaction(self, transaction_id: str) -> bool:
        """
        Removes a transaction by its ID and updates the balance.

        Args:
            transaction_id (str): The ID of the transaction to remove.

        Returns:
            bool: True if the transaction was found and removed, False otherwise.
        """
        # Use enumerate to get both the index and the object, which is efficient for deletion.
        for i, transaction in enumerate(self.transaction_list):
            if transaction.transaction_id == transaction_id:
                self._balance -= transaction.amount
                del self.transaction_list[i]
                print(f"Transaction {transaction_id} removed. New balance: ${self._balance:.2f}")
                return True
        print(f"Transaction {transaction_id} not found.")
        return False

    def get_balance(self) -> float:
        """
        Returns the current balance of the account.
        """
        return self._balance

    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """
        Retrieves all transactions belonging to a specific category.

        Args:
            category (str): The category to filter by.

        Returns:
            List[Transaction]: A list of matching Transaction objects.
        """
        # Using a list comprehension for a concise, efficient filter
        return [t for t in self.transaction_list if t.category.lower() == category.lower()]

    def get_monthly_summary(self) -> Dict[str, float]:
        """
        Calculates a summary of spending per category for the current month.

        Returns:
            Dict[str, float]: A dictionary mapping each category to its total spending.
        """
        current_month = datetime.now().month
        summary = {}
        for t in self.transaction_list:
            if t.date.month == current_month:
                # The .get() method is used to safely retrieve a value with a default of 0.
                summary[t.category] = summary.get(t.category, 0) + t.amount
        return summary

class CheckingAccount(Account):
    """
    A subclass of Account with specific features for a checking account,
    such as overdraft protection.
    """
    def __init__(self, account_name: str, initial_balance: float = 0.0, overdraft_limit: float = 500.0):
        # Call the parent class's constructor to initialize inherited attributes
        super().__init__(account_name, "Checking", initial_balance)
        self.overdraft_limit = overdraft_limit

    def add_transaction(self, transaction: Transaction):
        """
        Overrides the parent method to include overdraft protection logic.
        """
        if self._balance + transaction.amount < -self.overdraft_limit:
            print("Warning: Transaction would exceed overdraft limit. Transaction rejected.")
        else:
            # If the transaction is valid, call the parent's add_transaction method
            super().add_transaction(transaction)

class SavingsAccount(Account):
    """
    A subclass of Account with specific features for a savings account,
    such as an interest rate.
    """
    def __init__(self, account_name: str, initial_balance: float = 0.0, interest_rate: float = 0.01):
        # Call the parent class's constructor
        super().__init__(account_name, "Savings", initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        """
        Applies interest to the current balance.
        """
        self._balance *= (1 + self.interest_rate)
        print(f"Interest applied. New balance: ${self._balance:.2f}")

# Example Usage:
if __name__ == '__main__':
    # Create some dummy transactions
    t1 = Transaction('tx1', datetime(2025, 8, 1), -50.00, 'Groceries', 'Local Market')
    t2 = Transaction('tx2', datetime(2025, 8, 5), -1500.00, 'Rent', 'Landlord Inc.')
    t3 = Transaction('tx3', datetime(2025, 7, 20), 2000.00, 'Salary', 'Tech Co.')

    # Create a checking account and add transactions
    my_checking = CheckingAccount("Main Checking", initial_balance=100.0)
    my_checking.add_transaction(t1)
    my_checking.add_transaction(t2)
    my_checking.add_transaction(t3)

    # Test monthly summary
    print("\nMonthly Summary:")
    print(my_checking.get_monthly_summary())

    # Create a savings account and apply interest
    my_savings = SavingsAccount("Emergency Savings", initial_balance=5000.0, interest_rate=0.005)
    print(f"\nSavings balance before interest: ${my_savings.get_balance():.2f}")
    my_savings.apply_interest()
    print(f"Savings balance after interest: ${my_savings.get_balance():.2f}")
