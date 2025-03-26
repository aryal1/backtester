# strategy.py
import pandas as pd

class MovingAverageCrossStrategy:
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window
        self.signals = None

    def generate_signals(self, data: pd.DataFrame):
        """
        Creates signals DataFrame. For each date:
          - 1.0 => Buy signal
          - -1.0 => Sell signal
          - 0.0 => No action
        """
        signals = pd.DataFrame(index=data.index)
        signals['short_mavg'] = data['Close'].rolling(self.short_window).mean()
        signals['long_mavg'] = data['Close'].rolling(self.long_window).mean()
        # Initialize the signal column
        signals['signal'] = 0.0
        signals['signal'][self.short_window:] = \
            (signals['short_mavg'][self.short_window:] 
             > signals['long_mavg'][self.short_window:]).astype(float)
        # Generate trading orders by taking the difference of the signals
        signals['positions'] = signals['signal'].diff().fillna(0)
        self.signals = signals

        return signals
