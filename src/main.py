"""
Main entry point for the Time Series Analyzer application.

This script initializes the Tkinter root window and creates an instance
of the TimeSeriesAnalyzer class to run the application.
"""

import tkinter as tk
from time_series_analyzer import TimeSeriesAnalyzer

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeSeriesAnalyzer(root)
    root.mainloop()