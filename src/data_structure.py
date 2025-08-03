"""
This module demonstrates the implementation and use of various Python data structures,
including lists, dictionaries, tuples, sets, and nested structures.
"""

from typing import List, Dict, Any, Set, Tuple

### 1. Lists for Transaction Categories
def add_category(categories: List[str], new_category: str) -> List[str]:
    """
    Adds a new category to a list of categories.

    Args:
        categories: A list of existing category names.
        new_category: The new category name to add.

    Returns:
        The updated list of categories.
    """
    if new_category not in categories:
        categories.append(new_category)
        return categories

### 2. Use Dictionaries for Category Budgets

def set_budget(budgets: Dict[str,float],category:str,amount:float) -> Dict[str,float]:
    """
    Sets or updates the budget for a given category.

    Args:
        budgets: A dictionary mapping categories to budget amounts.
        category: The category to set the budget for.
        amount: The new budget amount.

    Returns:
        The updated budgets dictionary.
    """
    budgets[category] = amount
    return budgets


# 3 .Utilize tuples for immutable transaction records

def create_transaction_records(transaction_id: Any, date: str,amount:float,category:str) -> Tuple[Any,str,float,str]:
    """
       Creates an immutable transaction record as a tuple.

       Args:
           transaction_id: A unique identifier for the transaction.
           date: The date of the transaction (e.g., "YYYY-MM-DD").
           amount: The transaction amount.
           category: The category of the transaction.

       Returns:
           A tuple representing the immutable transaction record.
       """
    return (transaction_id, date, amount, category)






# 4. Create sets - unique merchant names
def add_merchants(merchants:Set[str], new_merchants:List[str]) -> Set[str]:
    """
    Adds new merchant names to a set, automatically handling duplicates.

    Args:
        merchants: A set of existing merchant names.
        new_merchants: A list of new merchant names to add.

    Returns:
        The updated set of unique merchant names.
    """
    merchants.update(new_merchants)
    return merchants


### 5. Nested Data Structures (List of Dictionaries)
def add_transaction_to_history(
        history: List[Dict[str, Any]],
        transaction: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Adds a new transaction dictionary to a list of transaction history.

    Args:
        history: A list of transaction dictionaries.
        transaction: A new transaction dictionary to add.

    Returns:
        The updated list of transaction history.
    """
    history.append(transaction)
    return history


# 6.search
def find_transactions_by_category(
        history: List[Dict[str, Any]],
        category: str
) -> List[Dict[str, Any]]:
    """
    Searches for and returns all transactions belonging to a specific category.

    Args:
        history: A list of transaction dictionaries.
        category: The category to search for.

    Returns:
        A new list containing only the transactions from the specified category.
    """
    return [t for t in history if t['category'] == category]



if __name__ == "__main__":
    categories = ["Groceries","entertainment","Utilities","House","Auto","Misc"]
    budgets = {"Groceries" : 800,"entertainment":100,"Utilities":500,"House":1400,"Auto":600,"Misc":50}
    merchants = {"target","Walmart"}
    transaction_history: List[Dict[str, Any]] = []




print("--- 1. Using Lists ---")
print(f"Initial categories: {categories}")
categories = add_category(categories, "Shopping")
print(f"Updated categories: {categories}")


print("--- 2. Using Dict ---")
print(f"Initial budget: {budgets}")
budgets = set_budget(budgets,"Groceries",600.00)
print(f"Updated budget: {budgets}")


print("------3. Using tuple----")
transaction_record_update = create_transaction_records(1,"01-01-2025",400,"Groceries")
print(f"transaction set {transaction_record_update}")

print("------4. Using Set----")
print(f"Intial Merchant:{merchants}")
merchants = add_merchants(merchants,["Netflix","Spotify"])
print(f"UpdatedMerchant set {merchants}")

print("--- 5. Using Nested Structures ---")
# Add transactions to history using dictionaries
transaction1 = {"id": 1, "date": "2025-08-05", "amount": 25.50, "category": "Groceries", "merchant": "Walmart"}
transaction_history = add_transaction_to_history(transaction_history, transaction1)
transaction2 = {"id": 2, "date": "2025-08-06", "amount": 15.00, "category": "Entertainment", "merchant": "Netflix"}
transaction_history = add_transaction_to_history(transaction_history, transaction2)


print("Full transaction history:")
for transaction in transaction_history:
    print(f"  - {transaction}")

print("\nFiltered transactions (Category: Groceries):")
groceries_transactions = find_transactions_by_category(transaction_history, "Groceries")
for transaction in groceries_transactions:
    print(f"  - {transaction}")


