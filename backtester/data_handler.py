# data_handler.py
import pandas as pd
import os

class DataHandler:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        """
        Loads data from a CSV into a pandas DataFrame. 
        Assumes the CSV has columns: Date, Open, High, Low, Close, Volume.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file {self.data_path} not found")

        self.data = pd.read_csv(self.data_path, parse_dates=["Date"], index_col="Date")
        self.data.sort_index(inplace=True)  # Ensure ascending date order

        return self.data
