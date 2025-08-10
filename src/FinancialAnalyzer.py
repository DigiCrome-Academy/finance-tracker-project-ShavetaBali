import numpy as np
from typing import Dict, List, Tuple

class FinancialAnalyzer:
    """
    A class for performing various financial and statistical analyses using NumPy.
    This class is designed to work with numerical data represented as arrays.
    """

    def __init__(self, data: np.ndarray):
        """
        Initializes the analyzer with a NumPy array of financial data.

        Args:
            data (np.ndarray): A 1D NumPy array of numerical data,
                               e.g., daily expenses or portfolio returns.
        """
        # Ensure the input is a NumPy array.
        if not isinstance(data, np.ndarray) or data.ndim != 1:
            raise ValueError("Data must be a 1D NumPy array.")
        self.data = data

    def calculate_moving_averages(self, window_size: int) -> np.ndarray:
        """
        Computes the moving average of the data over a specified window.

        Args:
            window_size (int): The number of data points to include in each average.

        Returns:
            np.ndarray: A NumPy array containing the moving averages.
        """
        if window_size <= 0 or window_size > len(self.data):
            raise ValueError("Invalid window size.")

        # NumPy's vectorized operations are highly efficient for this.
        # We create a convolution kernel and use np.convolve to compute the sum,
        # then divide by the window size. This is much faster than a Python loop.
        weights = np.ones(window_size) / window_size
        return np.convolve(self.data, weights, mode='valid')

    def analyze_spending_patterns(self) -> Dict[str, float]:
        """
        Performs a basic statistical analysis of the spending data.

        Returns:
            Dict[str, float]: A dictionary containing statistical metrics.
        """
        if len(self.data) == 0:
            return {"mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}

        # Use powerful NumPy functions for quick and accurate calculations.
        return {
            "mean": np.mean(self.data),
            "std_dev": np.std(self.data),
            "min": np.min(self.data),
            "max": np.max(self.data),
            "median": np.median(self.data),
            "q25": np.percentile(self.data, 25), # 25th percentile (first quartile)
            "q75": np.percentile(self.data, 75)  # 75th percentile (third quartile)
        }

    def project_future_balance(self, num_periods: int) -> float:
        """
        Projects a future balance using simple linear regression.

        Args:
            num_periods (int): The number of future periods to project.

        Returns:
            float: The projected balance at the end of the specified periods.
        """
        if len(self.data) < 2:
            return self.data[-1] if len(self.data) > 0 else 0.0

        # Create time indices for the data.
        x = np.arange(len(self.data))
        y = self.data

        # Use np.polyfit to find the best-fit line (linear regression).
        # It returns the coefficients of the polynomial (slope and intercept).
        slope, intercept = np.polyfit(x, y, 1)

        # The projected period is the last index plus the number of new periods.
        future_x = len(self.data) + num_periods - 1

        # Calculate the projected value.
        projected_balance = (slope * future_x) + intercept

        return projected_balance

    def calculate_portfolio_metrics(self, returns_data: np.ndarray, risk_free_rate: float = 0.02) -> Dict[str, float]:
        """
        Calculates key portfolio performance metrics.

        Args:
            returns_data (np.ndarray): A 1D array of portfolio returns.
            risk_free_rate (float): The annualized risk-free rate of return.

        Returns:
            Dict[str, float]: A dictionary of performance metrics.
        """
        if len(returns_data) == 0:
            return {"total_return": 0.0, "volatility": 0.0, "sharpe_ratio": 0.0}

        # Use vectorized NumPy operations for efficiency.
        total_return = np.sum(returns_data)
        volatility = np.std(returns_data) # Volatility is standard deviation of returns

        if volatility == 0:
            sharpe_ratio = 0.0
        else:
            # Sharpe ratio = (Average Return - Risk-Free Rate) / Volatility
            sharpe_ratio = (np.mean(returns_data) - risk_free_rate) / volatility

        return {
            "total_return": total_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio
        }

    def optimize_budget_allocation(self, spending_data: Dict[str, np.ndarray], total_budget: float) -> Dict[str, float]:
        """
        A simplified example of budget optimization using NumPy.
        It allocates budget based on a simple heuristic: categories with
        higher average spending get a larger proportional budget.

        Args:
            spending_data (Dict[str, np.ndarray]): Dictionary where keys are categories
                                                   and values are NumPy arrays of expenses.
            total_budget (float): The total budget to be allocated.

        Returns:
            Dict[str, float]: A dictionary showing the optimized budget for each category.
        """
        if not spending_data or total_budget <= 0:
            return {}

        # Use a vectorized operation to compute the mean for all categories at once.
        category_means = {cat: np.mean(expenses) for cat, expenses in spending_data.items()}

        # Calculate the sum of all average spending.
        total_mean_spending = sum(category_means.values())

        if total_mean_spending == 0:
            return {cat: total_budget / len(spending_data) for cat in spending_data}

        # Allocate the budget proportionally based on historical average spending.
        # This is a simple, vectorized operation.
        optimized_allocation = {
            cat: (mean_val / total_mean_spending) * total_budget
            for cat, mean_val in category_means.items()
        }

        return optimized_allocation


# Example usage
if __name__ == '__main__':
    # Sample daily expenses data
    daily_expenses = np.array([55.75, 12.50, 20.00, 85.30, 30.00, 15.00, 45.10, 60.00, 72.80, 25.00])
    analyzer = FinancialAnalyzer(daily_expenses)

    print("--- Spending Analysis ---")
    stats = analyzer.analyze_spending_patterns()
    print(f"Spending Statistics: {stats}")

    print("\n--- Moving Averages ---")
    moving_avg = analyzer.calculate_moving_averages(window_size=3)
    print(f"3-Day Moving Averages: {moving_avg}")

    print("\n--- Future Balance Projection ---")
    # For a simple projection, let's use a cumulative sum to simulate a balance over time.
    cumulative_expenses = np.cumsum(daily_expenses)
    balance_over_time = 1000 - cumulative_expenses

    balance_analyzer = FinancialAnalyzer(balance_over_time)
    projected_balance = balance_analyzer.project_future_balance(num_periods=5)
    print(f"Projected balance after 5 periods: ${projected_balance:.2f}")

    print("\n--- Portfolio Metrics ---")
    # Sample daily portfolio returns (e.g., 0.5% return, -0.2% loss, etc.)
    daily_returns = np.array([0.005, -0.002, 0.01, 0.008, -0.001, 0.003])
    metrics = analyzer.calculate_portfolio_metrics(daily_returns)
    print(f"Portfolio Metrics: Total Return={metrics['total_return']:.2%}, "
          f"Volatility={metrics['volatility']:.2%}, Sharpe Ratio={metrics['sharpe_ratio']:.2f}")

    print("\n--- Budget Optimization ---")
    # Sample historical spending data for different categories.
    spending_by_category = {
        "Groceries": np.array([55.75, 60.00, 58.20]),
        "Entertainment": np.array([12.50, 25.00, 15.00]),
        "Bills": np.array([200.00, 210.00, 195.00])
    }
    optimized_budget = analyzer.optimize_budget_allocation(spending_by_category, total_budget=500.00)
    print("Optimized Monthly Budget:")
    for cat, budget in optimized_budget.items():
        print(f"- {cat}: ${budget:.2f}")

