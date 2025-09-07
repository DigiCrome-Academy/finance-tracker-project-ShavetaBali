from datetime import datetime
import uuid

# The class is now a standard Python class
class Transaction:
    """
    Represents a single financial transaction.

    Attributes:
        transaction_id (str): A unique identifier for the transaction.
        date (datetime): The date and time of the transaction.
        amount (float): The amount of the transaction.
        category (str): The category of the transaction (e.g., 'Groceries', 'Rent').
        merchant (str): The name of the merchant.
        description (str): A brief description of the transaction.
        account_type (str): The type of account (e.g., 'Checking', 'Savings').
    """

    def __init__(self, date: datetime, amount: float, category: str,
                 merchant: str, description: str, account_type: str):
        """
        The constructor for the Transaction class. It performs validation
        and initializes the attributes.
        """
        self.transaction_id = str(uuid.uuid4())

        # Validate that the amount is a positive number.
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Transaction amount must be a positive number.")

        # Validate that required string fields are not empty.
        for arg, val in [('category', category), ('merchant', merchant),
                         ('description', description), ('account_type', account_type)]:
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"'{arg}' cannot be empty.")

        # Assign the validated attributes.
        self.date = date
        self.amount = amount
        self.category = category
        self.merchant = merchant
        self.description = description
        self.account_type = account_type

    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the transaction.
        """
        return (f"Transaction ID: {self.transaction_id}\n"
                f"Date: {self.date.strftime('%Y-%m-%d %H:%M')}\n"
                f"Amount: ${self.amount:.2f}\n"
                f"Category: {self.category}\n"
                f"Merchant: {self.merchant}\n"
                f"Description: {self.description}\n"
                f"Account: {self.account_type}")

    def __repr__(self) -> str:
        """
        Provides an unambiguous, developer-friendly string representation.
        This allows for easy re-creation of the object.
        """
        return (f"Transaction(date={repr(self.date)}, amount={self.amount}, "
                f"category='{self.category}', merchant='{self.merchant}', "
                f"description='{self.description}', account_type='{self.account_type}')")

    def __eq__(self, other) -> bool:
        """
        Implements the equality comparison operator (==).
        Transactions are considered equal if their IDs match.
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.transaction_id == other.transaction_id

    def __lt__(self, other) -> bool:
        """
        Implements the less-than comparison operator (<).
        Compares transactions based on their date.
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.date < other.date

    def __le__(self, other) -> bool:
        """
        Implements the less-than-or-equal-to comparison operator (<=).
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.date <= other.date

    def to_dict(self) -> dict:
        """
        Serializes the transaction object into a dictionary,
        making it easy to save to a file or database.
        """
        return {
            "transaction_id": self.transaction_id,
            "date": self.date.isoformat(),
            "amount": self.amount,
            "category": self.category,
            "merchant": self.merchant,
            "description": self.description,
            "account_type": self.account_type
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        A class method to deserialize a dictionary back into a Transaction object.
        """
        data['date'] = datetime.fromisoformat(data['date'])
        # Instantiate the class with the data, excluding the ID since it's generated internally
        # We must create an instance with the required parameters first, then manually set the ID
        transaction = cls(
            date=data['date'],
            amount=data['amount'],
            category=data['category'],
            merchant=data['merchant'],
            description=data['description'],
            account_type=data['account_type']
        )
        transaction.transaction_id = data['transaction_id']
        return transaction


    @property
    def year(self) -> int:
        """
        A property decorator to compute and return the year of the transaction.
        """
        return self.date.year

    @property
    def month(self) -> int:
        """
        A property decorator to compute and return the month of the transaction.
        """
        return self.date.month

    @property
    def day(self) -> int:
        """
        A property decorator to compute and return the day of the transaction.
        """
        return self.date.day

# Example usage of the Transaction class
if __name__ == '__main__':
    # Creating a valid transaction
    try:
        t1 = Transaction(
            date=datetime(2023, 8, 9, 10, 30),
            amount=55.75,
            category="Groceries",
            merchant="Whole Foods",
            description="Weekly groceries",
            account_type="Checking"
        )
        print("Successfully created a valid transaction:")
        print(t1)
        print("-" * 20)

        # Demonstrating computed properties
        print(f"Transaction Year: {t1.year}")
        print(f"Transaction Month: {t1.month}")
        print(f"Transaction Day: {t1.day}")
        print("-" * 20)

        # Demonstrating comparison
        t2 = Transaction(
            date=datetime(2023, 8, 8, 9, 0),
            amount=25.00,
            category="Dining",
            merchant="Coffee Shop",
            description="Morning coffee",
            account_type="Checking"
        )
        print("Creating a second transaction for comparison:")
        print(t2)
        print(f"Is t2 older than t1? {t2 < t1}")
        print("-" * 20)

        # Demonstrating serialization
        t1_dict = t1.to_dict()
        print("Serialized to a dictionary:")
        print(t1_dict)
        print("-" * 20)

        # Demonstrating deserialization
        t3 = Transaction.from_dict(t1_dict)
        print("Deserialized from a dictionary:")
        print(t3)
        print(f"Are t1 and t3 equal? {t1 == t3}")
        print("-" * 20)


    except ValueError as e:
        print(f"Error creating transaction: {e}")

    # Example of invalid transaction (negative amount)
    try:
        print("Attempting to create a transaction with a negative amount...")
        t_invalid = Transaction(
            date=datetime.now(),
            amount=-100,
            category="Test",
            merchant="Test Merchant",
            description="Invalid transaction",
            account_type="Checking"
        )
    except ValueError as e:
        print(f"Successfully caught an error: {e}")