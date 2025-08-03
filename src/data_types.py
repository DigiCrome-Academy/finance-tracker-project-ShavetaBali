"""
This module contains functions that demonstrate the use of basic Python data types
and perform common data manipulation tasks.
"""

from typing import List
from datetime import datetime

### 1. Primitive Data Type Functions

def demonstrate_primitives(
        integer_val: int,
        float_val: float,
        string_val: str,
        boolean_val: bool
) -> str:
    """

    :param integer_val:
    :param float_val:
    :param string_val:
    :param boolean_val:
    :return:
    """
    return(
f"Integer:{integer_val} (Type:{type(integer_val).__name__})\n"
f"Float:{float_val}(Type:{type(float_val)})\n"
f"String:{string_val}(Type{type(string_val)})\n"
f"Boolean{boolean_val}(type{type(boolean_val)})"
    )



# 2 . convert currency
def convert_currency_to_float(currency:str) -> float:
    """

    :param currency:
    :return:
    """
    print(f"Initial string: '{currency}'")

    try:
        # Loop 1: Remove leading non-digit characters
        while currency and not currency[0].isdigit():
            currency = currency[1:]

        # Loop 2: Remove trailing non-digit characters
        while currency and not currency[-1].isdigit():
            currency = currency[:-1]

        # Replace commas with an empty string
        currency = currency.replace(',', "")
        print(f"updated string: '{currency}'")

        return float(currency)

    except (ValueError, TypeError):
        print(f"Error: Could not convert '{currency}' to a float.")
        return None



# 3 . Calculate Percentage
def calculate_percentage(part,whole) :
    """

    :param part:
    :param whole:
    :return:
    """
    if whole==0.0:
        return 0
    else :
        percentage = (part/whole)*100
        print(f"Percentage {percentage}")
        return percentage



# 4. Date Validation Function

def validate_date(date_string: str):
        """

        :param date_string:
        :return:
        """
        formats : List[str] = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"]
        for fmt in formats :
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
                print(f"Error:invalid date format for {date_string}")
                return None



print("--- Demonstrating Primitives ---")
print(demonstrate_primitives(100, 3.14, "Hello, Python", True))


print("\n--- Currency convert  ---")
print(convert_currency_to_float("$12,000"))

print("\n--- Calculate Percentage  ---")
print(calculate_percentage(10,20))



print("\n--- Validating Dates ---")
date_str1 = "2025-08-05"
date_str2 = "08/05/2025"
invalid_date = "2025-13-40"

print(f"Date '{date_str1}' is valid: {validate_date(date_str1)}")
print(f"Date '{date_str2}' is valid: {validate_date(date_str2)}")
print(f"Date '{invalid_date}' is valid: {validate_date(invalid_date)}")


