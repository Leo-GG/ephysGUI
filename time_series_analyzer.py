"""
TimeSeriesAnalyzer class for analyzing and visualizing time series data.

This module contains the main application logic for loading, processing,
and visualizing time series data. It integrates the GUI components and
data processing functions to provide a complete analysis tool.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from gui_components import create_style, create_file_section, create_channel_section, create_artifact_section, create_peak_section
from data_processor import apply_filters, run_artifact_detection, run_peak_detection

class TimeSeriesAnalyzer:
    """
    A class for analyzing and visualizing time series data.

    This class provides methods for loading data, detecting artifacts,
    detecting peaks, and visualizing the results.
    """

    def __init__(self, master):
        """
        Initialize the TimeSeriesAnalyzer.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        self.master.title("Time Series Analyzer")
        self.master.geometry("1200x800")
        self.master.configure(bg='#2b2b2b')

        self.data = None
        self.filtered_data = None
        self.peaks = None
        self.extracted_signals = None
        self.artifact_indices = None

        self.style = create_style()
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """Create and initialize all GUI widgets."""
        self.file_frame, self.load_button = create_file_section(self.master, self.load_data)
        self.channel_frame, self.channel_var, self.channel_label, self.channel_menu = create_channel_section(self.master, self.plot_data)
        self.artifact_frame, self.artifact_threshold, self.artifact_button = create_artifact_section(self.master, self.run_artifact_detection)
        self.peak_frame, self.peak_height, self.peak_distance, self.peak_button = create_peak_section(self.master, self.run_peak_detection)

        self.info_frame = tk.Frame(self.master, bg='#2b2b2b', padx=10, pady=5)
        self.info_label = tk.Label(self.info_frame, text="", font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.info_label.pack()

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#3c3c3c')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()

    def create_layout(self):
        """Arrange the GUI widgets in the application window."""
        self.file_frame.pack(fill="x", padx=10, pady=5)
        self.channel_frame.pack(fill="x", padx=10, pady=5)
        self.artifact_frame.pack(fill="x", padx=10, pady=5)
        self.peak_frame.pack(fill="x", padx=10, pady=5)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

    def load_data(self):
        """
        Load time series data from a CSV file and apply pre-processing filters.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path, index_col=0)
                # Apply pre-processing filters
                self.data = apply_filters(self.data)
                self.channel_menu['values'] = ['All'] + list(self.data.columns)
                self.channel_var.set('All')
                self.plot_data()
                messagebox.showinfo("Data Loaded", "Data has been loaded and pre-processed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the data: {str(e)}")

    def plot_data(self):
        """Plot the loaded or processed time series data."""
        self.ax.clear()
        if self.data is not None:
            if self.channel_var.get() == 'All':
                self.data.plot(ax=self.ax)
            else:
                self.data[self.channel_var.get()].plot(ax=self.ax)
            self.ax.set_title("Pre-processed Time Series Data", fontsize=16)
            self.ax.set_xlabel("Time", fontsize=14)
            self.ax.set_ylabel("Amplitude", fontsize=14)
            self.ax.tick_params(axis='both', which='major', labelsize=12)
            self.canvas.draw()

    def run_artifact_detection(self):
        """
        Run artifact detection on the loaded data and update the plot.
        """
        if self.data is None:
            messagebox.showwarning("No Data", "Please load data before running artifact detection.")
            return
        threshold = float(self.artifact_threshold.get())
        self.filtered_data, artifact_count, self.artifact_indices = run_artifact_detection(self.data, threshold)
        self.plot_data_with_artifacts()
        self.info_label.config(text=f"Artifacts detected: {artifact_count}")
        messagebox.showinfo("Artifact Detection", f"Artifact detection completed. {artifact_count} artifacts found.")

    def plot_data_with_artifacts(self):
        """Plot the time series data with detected artifacts marked."""
        self.ax.clear()
        if self.channel_var.get() == 'All':
            for column in self.filtered_data.columns:
                self.ax.plot(self.filtered_data.index, self.filtered_data[column], label=column)
                self.ax.scatter(self.artifact_indices[column], self.filtered_data.loc[self.artifact_indices[column], column], 
                                color='red', marker='x', s=100, label=f'{column} Artifacts')
            self.ax.legend(fontsize=12)
        else:
            column = self.channel_var.get()
            self.ax.plot(self.filtered_data.index, self.filtered_data[column])
            self.ax.scatter(self.artifact_indices[column], self.filtered_data.loc[self.artifact_indices[column], column], 
                            color='red', marker='x', s=100, label='Artifacts')
            self.ax.legend(fontsize=12)
        
        self.ax.set_title("Filtered Data with Detected Artifacts", fontsize=16)
        self.ax.set_xlabel("Time", fontsize=14)
        self.ax.set_ylabel("Amplitude", fontsize=14)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.canvas.draw()

    def run_peak_detection(self):
        """
        Run peak detection on the filtered data and update the plot.
        """
        if self.filtered_data is None:
            messagebox.showwarning("No Filtered Data", "Please run artifact detection before peak detection.")
            return
        height = float(self.peak_height.get())
        distance = int(self.peak_distance.get())
        self.peaks, self.extracted_signals, peak_count = run_peak_detection(self.filtered_data, height, distance, self.artifact_indices)
        self.plot_peaks()
        self.info_label.config(text=f"Peaks detected: {peak_count}")
        messagebox.showinfo("Peak Detection", f"Peak detection completed. {peak_count} peaks found.")

    def plot_peaks(self):
        """Plot the filtered data with detected peaks and artifacts marked."""
        self.ax.clear()
        if self.channel_var.get() == 'All':
            for column in self.filtered_data.columns:
                self.ax.plot(self.filtered_data.index, self.filtered_data[column], label=column)
                self.ax.scatter(self.peaks[column], self.filtered_data.loc[self.peaks[column], column], 
                                color='green', marker='o', s=100, label=f'{column} Peaks')
                self.ax.scatter(self.artifact_indices[column], self.filtered_data.loc[self.artifact_indices[column], column], 
                                color='red', marker='x', s=100, label=f'{column} Artifacts')
            self.ax.legend(fontsize=12)
        else:
            column = self.channel_var.get()
            self.ax.plot(self.filtered_data.index, self.filtered_data[column])
            self.ax.scatter(self.peaks[column], self.filtered_data.loc[self.peaks[column], column], 
                            color='green', marker='o', s=100, label='Peaks')
            self.ax.scatter(self.artifact_indices[column], self.filtered_data.loc[self.artifact_indices[column], column], 
                            color='red', marker='x', s=100, label='Artifacts')
            self.ax.legend(fontsize=12)
        
        self.ax.set_title("Filtered Data with Detected Peaks and Artifacts", fontsize=16)
        self.ax.set_xlabel("Time", fontsize=14)
        self.ax.set_ylabel("Amplitude", fontsize=14)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.canvas.draw()

        self.plot_extracted_signals()

    def plot_extracted_signals(self):
        """Plot the extracted signals around detected peaks."""
        if self.extracted_signals is None:
            return

        extracted_fig, extracted_ax = plt.subplots(figsize=(10, 6))
        extracted_fig.patch.set_facecolor('#2b2b2b')
        extracted_ax.set_facecolor('#3c3c3c')
        extracted_ax.tick_params(colors='white', labelsize=12)
        extracted_ax.xaxis.label.set_color('white')
        extracted_ax.yaxis.label.set_color('white')
        extracted_ax.title.set_color('white')

        for column in self.extracted_signals:
            mean_signal = self.extracted_signals[column].mean(axis=0)
            extracted_ax.plot(mean_signal, label=f"{column} (Mean)")
            for signal in self.extracted_signals[column]:
                extracted_ax.plot(signal, alpha=0.1)

        extracted_ax.set_title("Extracted Signals Around Peaks", fontsize=16)
        extracted_ax.set_xlabel("Sample", fontsize=14)
        extracted_ax.set_ylabel("Amplitude", fontsize=14)
        extracted_ax.legend(fontsize=12)
        plt.show()