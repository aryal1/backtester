# utils.py
import numpy as np

def calculate_performance_metrics(equity_curve, freq='D'):
    """
    equity_curve: pd.Series of daily (or chosen freq) portfolio values
    freq: 'D' daily, 'M' monthly, etc. for annualizing returns
    """
    returns = equity_curve.pct_change().fillna(0)

    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1.0

    # Number of periods per year for freq
    if freq == 'D':
        periods_per_year = 252
    elif freq == 'W':
        periods_per_year = 52
    elif freq == 'M':
        periods_per_year = 12
    else:
        periods_per_year = 252  # default to daily

    # Annualized Return
    annualized_return = (1 + total_return) ** (periods_per_year / len(returns)) - 1

    # Annualized Volatility
    annualized_volatility = returns.std() * np.sqrt(periods_per_year)

    # Sharpe Ratio (risk-free rate assumed 0 for simplicity)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0

    # Max Drawdown
    rolling_max = equity_curve.cummax()
    drawdown = equity_curve / rolling_max - 1
    max_drawdown = drawdown.min()

    return {
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Annualized Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown
    }
