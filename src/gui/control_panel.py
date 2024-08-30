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

class ControlPanel(ttk.Frame):
    """
    Control panel for the Electrophysiology Data Analyzer.

    This class creates and manages the control widgets for data loading,
    filtering, artifact detection, and peak detection. It handles user inputs
    and processes the data accordingly.

    Attributes:
        update_callback (function): Callback function to update the plot.
        data (numpy.ndarray): Loaded electrophysiological data.
        time (numpy.ndarray): Time array corresponding to the data.
        sampling_rate (float): Sampling rate of the data in Hz.
        artifacts (numpy.ndarray): Boolean array indicating detected artifacts.
        peaks (list): List of arrays containing detected peak indices for each channel.
        peak_windows (list): List of arrays containing peak windows for each channel.
        avg_peak_windows (list): List of arrays containing average peak windows for each channel.
    """

    def __init__(self, parent):
        """
        Initialize the ControlPanel.

        Args:
            parent (tk.Widget): The parent widget for this panel.
            update_callback (function): Callback function to update the plot.
        """
        super().__init__(parent, style="Dark.TFrame", width=250)
        self.pack_propagate(False)

        self.plot_panel = PlotPanel(parent, self.update_trim_button)
        self.plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.statistics_panel = StatisticsPanel(parent)
        self.statistics_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.data = None
        self.time = None
        self.sampling_rate = None
        self.artifacts = None
        self.peaks = None
        self.peak_windows = None
        self.avg_peak_windows = None
        self.channel_mapping = []  # Add this line to store original channel numbers

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the control widgets."""
        self.configure(style="Dark.TFrame")
        self.create_filter_options()
        self.create_channel_selection()

        # Add Toggle Span Selector button
        self.toggle_span_button = ttk.Button(self, text="Toggle Span Selector", command=self.toggle_span_selector, style="Dark.TButton")
        self.toggle_span_button.pack(fill=tk.X, pady=5)

        # Add Trim Data button
        self.trim_button = ttk.Button(self, text="Trim Data", command=self.trim_data, style="Dark.TButton", state=tk.DISABLED)
        self.trim_button.pack(fill=tk.X, pady=5)

    def create_filter_options(self):
        """Create widgets for filter options, artifact detection, and peak detection."""
        filter_frame = ttk.Frame(self, style="Dark.TFrame")
        filter_frame.pack(fill=tk.X, pady=(0, 20))

        # Sampling rate
        sr_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        sr_frame.pack(fill=tk.X, pady=5)
        sr_label = ttk.Label(sr_frame, text="Sampling Rate (Hz):", style="Dark.TLabel")
        sr_label.pack(side=tk.LEFT)
        self.sr_entry = ttk.Entry(sr_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.sr_entry.pack(side=tk.RIGHT)
        self.sr_entry.insert(0, "20000")

        # Notch filter
        notch_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        notch_frame.pack(fill=tk.X, pady=5)
        notch_label = ttk.Label(notch_frame, text="Notch Filter (Hz):", style="Dark.TLabel")
        notch_label.pack(side=tk.LEFT)
        self.notch_entry = ttk.Entry(notch_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.notch_entry.pack(side=tk.RIGHT)
        self.notch_entry.insert(0, "50")
        notch_button = ttk.Button(filter_frame, text="Apply Notch", command=lambda: self.apply_filter('notch'), style="Dark.TButton")
        notch_button.pack(fill=tk.X, pady=5)

        # Low-pass filter
        lowpass_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        lowpass_frame.pack(fill=tk.X, pady=5)
        lowpass_label = ttk.Label(lowpass_frame, text="Low-pass Filter (Hz):", style="Dark.TLabel")
        lowpass_label.pack(side=tk.LEFT)
        self.lowpass_entry = ttk.Entry(lowpass_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.lowpass_entry.pack(side=tk.RIGHT)
        self.lowpass_entry.insert(0, "100")
        lowpass_button = ttk.Button(filter_frame, text="Apply Low-pass", command=lambda: self.apply_filter('lowpass'), style="Dark.TButton")
        lowpass_button.pack(fill=tk.X, pady=5)

        # High-pass filter
        highpass_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        highpass_frame.pack(fill=tk.X, pady=5)
        highpass_label = ttk.Label(highpass_frame, text="High-pass Filter (Hz):", style="Dark.TLabel")
        highpass_label.pack(side=tk.LEFT)
        self.highpass_entry = ttk.Entry(highpass_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.highpass_entry.pack(side=tk.RIGHT)
        self.highpass_entry.insert(0, "1")
        highpass_button = ttk.Button(filter_frame, text="Apply High-pass", command=lambda: self.apply_filter('highpass'), style="Dark.TButton")
        highpass_button.pack(fill=tk.X, pady=5)

        # Artifact detection
        artifact_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        artifact_frame.pack(fill=tk.X, pady=5)
        artifact_label = ttk.Label(artifact_frame, text="Artifact Threshold:", style="Dark.TLabel")
        artifact_label.pack(side=tk.LEFT)
        self.artifact_entry = ttk.Entry(artifact_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.artifact_entry.pack(side=tk.RIGHT)
        self.artifact_entry.insert(0, "5")
        artifact_button = ttk.Button(filter_frame, text="Detect Artifacts", command=self.detect_artifacts, style="Dark.TButton")
        artifact_button.pack(fill=tk.X, pady=5)

        # Peak detection
        peak_frame = ttk.Frame(filter_frame, style="Dark.TFrame")
        peak_frame.pack(fill=tk.X, pady=5)
        peak_label = ttk.Label(peak_frame, text="Peak Threshold:", style="Dark.TLabel")
        peak_label.pack(side=tk.LEFT)
        self.peak_entry = ttk.Entry(peak_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.peak_entry.pack(side=tk.RIGHT)
        self.peak_entry.insert(0, "50")

        # Add checkbox for peak polarity
        self.peak_polarity_var = tk.BooleanVar(value=False)
        self.peak_polarity_check = ttk.Checkbutton(
            filter_frame,
            text="Detect Positive Peaks",
            variable=self.peak_polarity_var,
            style="Dark.TCheckbutton"
        )
        self.peak_polarity_check.pack(fill=tk.X, pady=5)

        peak_button = ttk.Button(filter_frame, text="Detect Peaks", command=self.detect_peaks, style="Dark.TButton")
        peak_button.pack(fill=tk.X, pady=5)

    def create_channel_selection(self):
        """Create the channel selection listbox and delete buttons."""
        channel_frame = ttk.Frame(self, style="Dark.TFrame")
        channel_frame.pack(fill=tk.BOTH, expand=True)

        channel_label = ttk.Label(channel_frame, text="Channels", style="Dark.TLabel")
        channel_label.pack(pady=(0, 10))

        self.channel_listbox = tk.Listbox(channel_frame, selectmode=tk.MULTIPLE, bg="#1E1E1E", fg="white", font=("Arial", 12))
        self.channel_listbox.pack(fill=tk.BOTH, expand=True)
        self.channel_listbox.bind("<<ListboxSelect>>", lambda event: self.update_callback())

        # Add Delete Channel button
        self.delete_channel_button = ttk.Button(channel_frame, text="Delete Selected Channels", command=self.delete_selected_channels, style="Dark.TButton")
        self.delete_channel_button.pack(fill=tk.X, pady=5)

        # Add Keep Selected Channels button
        self.keep_selected_button = ttk.Button(channel_frame, text="Keep Only Selected Channels", command=self.keep_selected_channels, style="Dark.TButton")
        self.keep_selected_button.pack(fill=tk.X, pady=5)

    def update_channel_list(self):
        """Update the channel listbox with the available channels."""
        self.channel_listbox.delete(0, tk.END)
        for i, original_channel in enumerate(self.channel_mapping):
            self.channel_listbox.insert(tk.END, f"Channel {original_channel}")

    def delete_selected_channels(self):
        """Delete the selected channels and update the data."""
        selected_indices = self.channel_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one channel to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected channels? This action cannot be undone.")
        if not confirm:
            return

        # Convert to list and sort in descending order to avoid index issues when deleting
        selected_indices = sorted(list(selected_indices), reverse=True)

        # Delete channels from data and related arrays
        for index in selected_indices:
            self.data = np.delete(self.data, index, axis=1)
            if self.artifacts is not None:
                self.artifacts = np.delete(self.artifacts, index, axis=1)
            if self.peaks is not None:
                del self.peaks[index]
            if self.peak_windows is not None:
                del self.peak_windows[index]
            if self.avg_peak_windows is not None:
                del self.avg_peak_windows[index]
            del self.channel_mapping[index]  # Remove the channel from mapping

        # Update channel list and statistics
        self.update_channel_list()
        self.channel_statistics = compute_channel_statistics(self.data)
        if self.peaks is not None:
            self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time)
        else:
            self.peak_statistics = None

        self.statistics_panel.update_statistics(
            channel_statistics=self.channel_statistics,
            peak_statistics=self.peak_statistics,
            channel_mapping=self.channel_mapping
        )
        self.update_callback()

        messagebox.showinfo("Info", "Selected channels have been deleted successfully.")

    def keep_selected_channels(self):
        """Delete all channels except the selected ones."""
        selected_indices = self.channel_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one channel to keep.")
            return

        confirm = messagebox.askyesno("Confirm Keep", "Are you sure you want to keep only the selected channels? This action cannot be undone.")
        if not confirm:
            return

        # Convert to set for faster lookup
        selected_indices_set = set(selected_indices)

        # Identify indices to delete (all except selected)
        indices_to_delete = [i for i in range(self.data.shape[1]) if i not in selected_indices_set]

        # Sort in descending order to avoid index issues when deleting
        indices_to_delete.sort(reverse=True)

        # Delete channels from data and related arrays
        for index in indices_to_delete:
            self.data = np.delete(self.data, index, axis=1)
            if self.artifacts is not None:
                self.artifacts = np.delete(self.artifacts, index, axis=1)
            if self.peaks is not None:
                del self.peaks[index]
            if self.peak_windows is not None:
                del self.peak_windows[index]
            if self.avg_peak_windows is not None:
                del self.avg_peak_windows[index]
            del self.channel_mapping[index]  # Remove the channel from mapping

        # Update channel list and statistics
        self.update_channel_list()
        self.channel_statistics = compute_channel_statistics(self.data)
        if self.peaks is not None:
            self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time)
        else:
            self.peak_statistics = None

        self.statistics_panel.update_statistics(
            channel_statistics=self.channel_statistics,
            peak_statistics=self.peak_statistics,
            channel_mapping=self.channel_mapping
        )
        self.update_callback()

        messagebox.showinfo("Info", "All channels except the selected ones have been deleted successfully.")

    def load_data(self):
        """Load data from a file and update the channel list."""
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.data, self.time = load_data(file_path)
            self.sampling_rate = float(self.sr_entry.get())
            self.time = self.time / self.sampling_rate
            self.channel_mapping = list(range(1, self.data.shape[1] + 1))  # Initialize channel mapping
            self.update_channel_list()
            
            # Compute and display channel statistics
            self.channel_statistics = compute_channel_statistics(self.data)
            self.statistics_panel.update_statistics(
                channel_statistics=self.channel_statistics,
                channel_mapping=self.channel_mapping
            )
            
            self.update_callback()

    def apply_filter(self, filter_type):
        """
        Apply a filter to the data.

        Args:
            filter_type (str): The type of filter to apply ('notch', 'lowpass', 'highpass').
        """
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            if filter_type == 'notch':
                freq = float(self.notch_entry.get())
                self.data = apply_notch_filter(self.data, self.sampling_rate, freq)
            elif filter_type == 'lowpass':
                freq = float(self.lowpass_entry.get())
                self.data = apply_lowpass_filter(self.data, self.sampling_rate, freq)
            elif filter_type == 'highpass':
                freq = float(self.highpass_entry.get())
                self.data = apply_highpass_filter(self.data, self.sampling_rate, freq)
            self.update_callback()
        except ValueError:
            messagebox.showerror("Error", f"Invalid {filter_type} frequency.")

    def detect_artifacts(self):
        """Detect artifacts in the data."""
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            threshold = float(self.artifact_entry.get())
            self.artifacts = detect_artifacts_all_channels(self.data, threshold=threshold)
            self.update_callback()
        except ValueError:
            messagebox.showerror("Error", "Invalid artifact threshold.")

    def detect_peaks(self):
        """Detect peaks in the data."""
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            threshold = float(self.peak_entry.get())
            window_size = int(self.sampling_rate * 0.1)  # 100ms window
            detect_positive = self.peak_polarity_var.get()
            
            print(f"Threshold: {threshold}")
            print(f"Data shape: {self.data.shape}")
            print(f"Sampling rate: {self.sampling_rate}")
            print(f"Detecting {'positive' if detect_positive else 'negative'} peaks")
            
            self.peaks = []
            self.peak_windows = []
            self.avg_peak_windows = []
            
            for channel in range(self.data.shape[1]):
                channel_data = self.data[:, channel]
                channel_peaks = detect_peaks(channel_data, self.sampling_rate, threshold, 
                                             detect_positive=detect_positive, window_size=window_size)
                
                self.peaks.append(channel_peaks)
                
                channel_peak_windows = extract_peak_windows(channel_data, channel_peaks, window_size)
                self.peak_windows.append(channel_peak_windows)
                
                if len(channel_peak_windows) > 0:
                    self.avg_peak_windows.append(np.mean(channel_peak_windows, axis=0))
                else:
                    self.avg_peak_windows.append(None)
            
            # Compute peak statistics
            self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time)
            self.statistics_panel.update_statistics(
                peak_statistics=self.peak_statistics,
                channel_mapping=self.channel_mapping
            )
            
            self.update_callback()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during peak detection: {str(e)}")

    def get_data(self):
        """
        Get the processed data and related information.

        Returns:
            dict: Dictionary containing the data, time, artifacts, peaks, peak windows, and selected channels.
        """
        return {
            'data': self.data,
            'time': self.time,
            'artifacts': self.artifacts,
            'peaks': self.peaks,
            'peak_windows': self.peak_windows,
            'avg_peak_windows': self.avg_peak_windows,
            'selected_channels': self.get_selected_channels(),
            'peak_statistics': self.peak_statistics if hasattr(self, 'peak_statistics') else None
        }

    def get_selected_channels(self):
        """
        Get the indices of the selected channels.

        Returns:
            list: List of indices of the selected channels.
        """
        return [self.channel_mapping[i] - 1 for i in self.channel_listbox.curselection()]

    def update_callback(self, event=None):
        data_dict = self.get_data()
        self.plot_panel.update_plot(data_dict)

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
            start_idx = np.searchsorted(self.time, self.selected_range[0])
            end_idx = np.searchsorted(self.time, self.selected_range[1])

            self.data = self.data[start_idx:end_idx]
            self.time = self.time[start_idx:end_idx]

            if self.artifacts is not None:
                self.artifacts = self.artifacts[start_idx:end_idx]

            if self.peaks is not None:
                self.peaks = [np.array([p for p in channel_peaks if start_idx <= p < end_idx]) - start_idx for channel_peaks in self.peaks]
            else:
                self.peaks = None

            if self.peak_windows is not None:
                self.peak_windows = [windows[np.logical_and(start_idx <= peaks, peaks < end_idx)] for windows, peaks in zip(self.peak_windows, self.peaks)]
            else:
                self.peak_windows = None

            if self.avg_peak_windows is not None:
                # Recalculate average peak windows if necessary
                self.avg_peak_windows = [np.mean(windows, axis=0) if len(windows) > 0 else None for windows in self.peak_windows]
            else:
                self.avg_peak_windows = None

            # Disable span selector and update plot
            self.plot_panel.span_selector_active = False
            self.plot_panel.remove_span_selector()
            self.toggle_span_button.config(text="Enable Span Selector")
            self.update_callback()

            # Recompute and update statistics
            self.channel_statistics = compute_channel_statistics(self.data)
            if self.peaks is not None:
                self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time)
            else:
                self.peak_statistics = None
            self.statistics_panel.update_statistics(
                channel_statistics=self.channel_statistics,
                peak_statistics=self.peak_statistics,
                channel_mapping=self.channel_mapping
            )

            messagebox.showinfo("Info", "Data has been trimmed successfully.")

    def save_statistics_to_excel(self):
        """Save the current statistics to an Excel file."""
        if not hasattr(self, 'channel_statistics'):
            messagebox.showwarning("Warning", "No statistics available to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return  # User cancelled the file dialog

        try:
            with pd.ExcelWriter(file_path) as writer:
                # Save channel statistics
                channel_df = pd.DataFrame(self.channel_statistics)
                channel_df['Original Channel'] = self.channel_mapping
                channel_df = channel_df.set_index('Original Channel')
                channel_df.to_excel(writer, sheet_name='Channel Statistics')

                # Save peak statistics if available
                if hasattr(self, 'peak_statistics') and self.peak_statistics:
                    peak_df = pd.DataFrame(self.peak_statistics)
                    peak_df['Original Channel'] = self.channel_mapping
                    peak_df = peak_df.set_index('Original Channel')
                    peak_df.to_excel(writer, sheet_name='Peak Statistics')
                else:
                    messagebox.showwarning("Warning", "No peak statistics available. Only channel statistics will be saved.")

            messagebox.showinfo("Success", f"Statistics saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")