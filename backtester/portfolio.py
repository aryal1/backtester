# portfolio.py
import pandas as pd

class Portfolio:
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize the portfolio with initial capital (e.g., $100,000).
        """
        self.initial_capital = initial_capital
        self.current_cash = initial_capital
        self.positions = 0  # For a single asset, track shares or units
        self.position_value = 0.0
        self.portfolio_history = []  # to store equity curve

    def update_market_value(self, price: float):
        """
        Update the market value of the held position based on current price.
        """
        self.position_value = self.positions * price

    def update_portfolio(self, date, price: float):
        """
        Store the daily portfolio value for reporting.
        """
        total_value = self.current_cash + self.position_value
        self.portfolio_history.append({
            'date': date,
            'total_value': total_value,
            'positions': self.positions,
            'cash': self.current_cash
        })

    def execute_trade(self, price: float, units: int):
        """
        Executes a trade, updates positions and cash.
        - `units` > 0 for buy
        - `units` < 0 for sell
        """
        cost = price * units
        # Update cash
        self.current_cash -= cost
        # Update positions
        self.positions += units

    def to_dataframe(self):
        """
        Convert the portfolio history to a Pandas DataFrame for analysis.
        """
        df = pd.DataFrame(self.portfolio_history)
        df.set_index('date', inplace=True)
        return df
