import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.data_handling.data_loader import load_data
from src.analysis.signal_processing import apply_notch_filter, apply_lowpass_filter, apply_highpass_filter, detect_peaks, extract_peak_windows
from src.analysis.artifact_detection import detect_artifacts_all_channels
import numpy as np
from .plot_panel import PlotPanel
from src.analysis.peak_statistics import compute_peak_statistics, compute_channel_statistics
from .statistics_panel import StatisticsPanel
import pandas as pd
from .data_manager import DataManager
from .filter_panel import FilterPanel
from .channel_panel import ChannelPanel

class ControlPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Dark.TFrame", width=250)
        self.pack_propagate(False)

        self.data_manager = DataManager(self.update_callback)
        
        self.plot_panel = PlotPanel(parent, self.update_trim_button)
        self.plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.statistics_panel = StatisticsPanel(parent)
        self.statistics_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.filter_panel = FilterPanel(self, self.data_manager, self.update_callback)
        self.filter_panel.pack(fill=tk.X, pady=10)

        self.channel_panel = ChannelPanel(self, self.data_manager, self.update_callback)
        self.channel_panel.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.configure(style="Dark.TFrame")
        
        # Add Toggle Span Selector button
        self.toggle_span_button = ttk.Button(self, text="Toggle Span Selector", command=self.toggle_span_selector, style="Dark.TButton")
        self.toggle_span_button.pack(fill=tk.X, pady=5)

        # Add Trim Data button
        self.trim_button = ttk.Button(self, text="Trim Data", command=self.trim_data, style="Dark.TButton", state=tk.DISABLED)
        self.trim_button.pack(fill=tk.X, pady=5)

    def load_data(self):
        sampling_rate = self.filter_panel.get_sampling_rate()
        self.data_manager.load_data(sampling_rate)
        self.channel_panel.update_channel_list()
        self.update_callback()

    def save_statistics_to_excel(self):
        if self.data_manager.channel_statistics is None:
            messagebox.showwarning("Warning", "No channel statistics available. Please load data first.")
            return
        self.data_manager.save_statistics_to_excel()

    def toggle_span_selector(self):
        self.plot_panel.toggle_span_selector()
        if self.plot_panel.span_selector_active:
            self.toggle_span_button.config(text="Disable Span Selector")
        else:
            self.toggle_span_button.config(text="Enable Span Selector")

    def update_trim_button(self, selected_range):
        self.selected_range = selected_range
        self.trim_button.config(state=tk.NORMAL if selected_range is not None else tk.DISABLED)

    def trim_data(self):
        if self.selected_range is None:
            messagebox.showwarning("Warning", "Please select a range first.")
            return

        confirm = messagebox.askyesno("Confirm Trim", "Are you sure you want to trim the data? This action cannot be undone.")
        if confirm:
            start_idx = np.searchsorted(self.data_manager.time, self.selected_range[0])
            end_idx = np.searchsorted(self.data_manager.time, self.selected_range[1])

            self.data_manager.trim_data(start_idx, end_idx)

            # Disable span selector and update plot
            self.plot_panel.span_selector_active = False
            self.plot_panel.remove_span_selector()
            self.toggle_span_button.config(text="Enable Span Selector")
            self.update_callback()

            messagebox.showinfo("Info", "Data has been trimmed successfully.")

    def update_callback(self, event=None):
        data_dict = self.data_manager.get_data()
        self.plot_panel.update_plot(data_dict)
        self.statistics_panel.update_statistics(
            channel_statistics=self.data_manager.channel_statistics,
            peak_statistics=self.data_manager.peak_statistics,
            channel_mapping=self.data_manager.channel_mapping
        )
