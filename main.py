# main.py
from backtester.backtest import Backtest

if __name__ == "__main__":
    data_path = "data/historical_data.csv"
    backtest = Backtest(
        data_path=data_path, 
        initial_capital=100000.0, 
        short_window=50, 
        long_window=200
    )
    results = backtest.run_backtest()
    backtest.plot_results()
