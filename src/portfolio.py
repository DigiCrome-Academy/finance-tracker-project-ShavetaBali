from datetime import date
from typing import Dict, List, Optional

# Nesting the Holding class within InvestmentPortfolio is a great way
# to show that a Holding only exists in the context of a portfolio.
class InvestmentPortfolio:
    """
    Manages a collection of investment holdings and a cash balance.
    This class demonstrates composition, as it is composed of Holding objects.
    """

    class Holding:
        """
        Represents an individual investment (e.g., a stock).
        This is a nested class, tightly coupled to the InvestmentPortfolio.
        """
        def __init__(self, symbol: str, shares: float, purchase_price: float, purchase_date: date):
            """
            Initializes a new investment holding.
            """
            if shares <= 0 or purchase_price <= 0:
                raise ValueError("Shares and purchase price must be positive.")
            self.symbol: str = symbol
            self.shares: float = shares
            self.purchase_price: float = purchase_price
            self.current_price: float = purchase_price # Initialize current price to purchase price
            self.purchase_date: date = purchase_date

        def get_value(self) -> float:
            """
            Calculates the current market value of the holding.
            """
            return self.shares * self.current_price

        def get_gain_loss(self) -> float:
            """
            Calculates the total profit or loss of the holding.
            """
            return (self.current_price - self.purchase_price) * self.shares

    def __init__(self, portfolio_name: str, cash_balance: float = 0.0):
        """
        Initializes a new InvestmentPortfolio.
        """
        if cash_balance < 0:
            raise ValueError("Cash balance cannot be negative.")
        self.portfolio_name: str = portfolio_name
        self.holdings: Dict[str, self.Holding] = {}
        self.cash_balance: float = cash_balance

    def add_holding(self, symbol: str, shares: float, purchase_price: float, purchase_date: date):
        """
        Adds a new holding to the portfolio.
        """
        if symbol in self.holdings:
            print(f"Warning: Holding for {symbol} already exists. Use update_holding to modify.")
            return

        new_holding = self.Holding(symbol, shares, purchase_price, purchase_date)
        self.holdings[symbol] = new_holding
        print(f"Added {shares} shares of {symbol} to the portfolio.")

    def remove_holding(self, symbol: str) -> Optional[Holding]:
        """
        Removes a holding from the portfolio by its symbol.
        """
        if symbol in self.holdings:
            removed_holding = self.holdings.pop(symbol)
            # A real-world application would likely move the proceeds to cash balance here.
            print(f"Removed holding for {symbol}.")
            return removed_holding
        print(f"Holding for {symbol} not found.")
        return None

    def update_prices(self, new_prices: Dict[str, float]):
        """
        Updates the current price for all holdings in the portfolio based on
        a dictionary of new prices. In a real application, this would likely
        come from a financial API.
        """
        for symbol, price in new_prices.items():
            if symbol in self.holdings:
                self.holdings[symbol].current_price = price
        print("Holding prices updated.")

    def calculate_total_value(self) -> float:
        """
        Calculates the total value of the portfolio, including cash and holdings.
        """
        holdings_value = sum(h.get_value() for h in self.holdings.values())
        return holdings_value + self.cash_balance

    def get_asset_allocation(self) -> Dict[str, float]:
        """
        Returns a dictionary of the percentage allocation of each asset.
        """
        total_value = self.calculate_total_value()
        if total_value == 0:
            return {}

        allocation = {symbol: (holding.get_value() / total_value) * 100
                      for symbol, holding in self.holdings.items()}

        # Add cash to the allocation.
        if self.cash_balance > 0:
            allocation['Cash'] = (self.cash_balance / total_value) * 100

        return allocation

    def get_portfolio_summary(self) -> Dict[str, float]:
        """
        A simple portfolio analytics method that returns a summary of
        performance metrics.
        """
        total_gain_loss = sum(h.get_gain_loss() for h in self.holdings.values())
        return {
            "total_value": self.calculate_total_value(),
            "total_gain_loss": total_gain_loss
        }

# Example usage of the InvestmentPortfolio class
if __name__ == '__main__':
    # Create a portfolio with an initial cash balance.
    my_portfolio = InvestmentPortfolio("Tech Portfolio", cash_balance=5000.0)

    # Add some initial holdings.
    my_portfolio.add_holding("MSFT", 10.0, 300.00, date(2022, 1, 15))
    my_portfolio.add_holding("GOOGL", 5.0, 150.00, date(2022, 2, 20))

    # Demonstrate portfolio summary before price updates.
    summary_before = my_portfolio.get_portfolio_summary()
    print("--- Portfolio Summary (Initial) ---")
    print(f"Total Value: ${summary_before['total_value']:.2f}")
    print(f"Total Gain/Loss: ${summary_before['total_gain_loss']:.2f}")

    print("\n--- Updating Prices ---")
    # Simulate a price update from an external source.
    market_prices = {"MSFT": 350.00, "GOOGL": 145.00}
    my_portfolio.update_prices(market_prices)

    # Demonstrate portfolio summary after price updates.
    summary_after = my_portfolio.get_portfolio_summary()
    print("\n--- Portfolio Summary (After Update) ---")
    print(f"Total Value: ${summary_after['total_value']:.2f}")
    print(f"Total Gain/Loss: ${summary_after['total_gain_loss']:.2f}")

    print("\n--- Asset Allocation ---")
    allocation = my_portfolio.get_asset_allocation()
    for asset, percentage in allocation.items():
        print(f"{asset}: {percentage:.2f}%")
