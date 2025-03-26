# backtest.py
from .data_handler import DataHandler
from .portfolio import Portfolio
from .strategy import MovingAverageCrossStrategy


class Backtest:
    def __init__(self, 
                 data_path, 
                 strategy_cls=MovingAverageCrossStrategy, 
                 initial_capital=100000.0, 
                 short_window=50, 
                 long_window=200):
        """
        - data_path: Path to CSV file with price data
        - strategy_cls: Strategy class to be instantiated
        - initial_capital: Starting cash
        - short_window, long_window: strategy parameters
        """
        self.data_path = data_path
        self.strategy_cls = strategy_cls
        self.initial_capital = initial_capital
        self.short_window = short_window
        self.long_window = long_window

        # Will be created during run_backtest
        self.data_handler = None
        self.strategy = None
        self.portfolio = None
        self.results = None

    def run_backtest(self):
        # 1. Load data
        self.data_handler = DataHandler(self.data_path)
        price_data = self.data_handler.load_data()

        # 2. Instantiate strategy and generate signals
        self.strategy = self.strategy_cls(self.short_window, self.long_window)
        signals = self.strategy.generate_signals(price_data)

        # 3. Instantiate portfolio
        self.portfolio = Portfolio(self.initial_capital)

        # 4. Simulate trading
        for current_date, row in signals.iterrows():
            price = price_data.loc[current_date, 'Close']
            position_change = row['positions']

            # If position_change == 1.0, it means we cross from 0 to 1 => buy signal
            if position_change == 1.0:
                # For demo: buy 1 unit (in real life you'd have a more 
                # sophisticated position sizing logic)
                self.portfolio.execute_trade(price, 1)

            elif position_change == -1.0:
                # Sell any current holdings (simplification)
                if self.portfolio.positions > 0:
                    self.portfolio.execute_trade(price, -self.portfolio.positions)

            # Update the portfolio's market value
            self.portfolio.update_market_value(price)
            self.portfolio.update_portfolio(current_date, price)

        # Convert portfolio history to DataFrame
        self.results = self.portfolio.to_dataframe()
        return self.results

    def plot_results(self):
        """
        Plots the portfolio's total value over time.
        """
        import matplotlib.pyplot as plt

        if self.results is None:
            raise ValueError("No results to plot. Please run the backtest first.")
        
        plt.figure()
        plt.plot(self.results.index, self.results['total_value'], label='Equity Curve')
        plt.legend()
        plt.title('Portfolio Value over Time')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.show()

'''# In backtest.py, after the loop
from utils import calculate_performance_metrics

def run_backtest(self):
    ...
    self.results = self.portfolio.to_dataframe()

    perf = calculate_performance_metrics(
        self.results['total_value'], freq='D'
    )
    print("Performance Metrics:")
    for k, v in perf.items():
        print(f"{k}: {v:0.2%}")

    return self.results'''
