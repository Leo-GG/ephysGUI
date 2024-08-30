import numpy as np
from tkinter import filedialog, messagebox
from src.data_handling.data_loader import load_data
from src.analysis.peak_statistics import compute_channel_statistics, compute_peak_statistics
import pandas as pd
import csv

class DataManager:
    """
    Manages the electrophysiology data and related operations.

    This class handles loading, processing, and storing of electrophysiology data,
    as well as various statistics and operations on the data.

    Attributes:
        update_callback (function): Callback function to update the GUI.
        data (numpy.ndarray): The electrophysiology data.
        time (numpy.ndarray): Time points corresponding to the data.
        sampling_rate (float): Sampling rate of the data in Hz.
        artifacts (numpy.ndarray): Detected artifacts in the data.
        peaks (list): Detected peaks for each channel.
        peak_windows (list): Extracted peak windows for each channel.
        avg_peak_windows (list): Average peak windows for each channel.
        channel_mapping (list): Mapping of original channel indices to current indices.
        channel_statistics (dict): Statistics for each channel.
        peak_statistics (dict): Statistics for detected peaks.
        selected_channels (list): Currently selected channels for analysis.
    """

    def __init__(self, update_callback):
        """
        Initialize the DataManager.

        Args:
            update_callback (function): Callback function to update the GUI.
        """
        self.update_callback = update_callback
        self.data = None
        self.time = None
        self.sampling_rate = None
        self.artifacts = None
        self.peaks = None
        self.peak_windows = None
        self.avg_peak_windows = None
        self.channel_mapping = []
        self.channel_statistics = None
        self.peak_statistics = None
        self.selected_channels = []

    def load_data(self, sampling_rate):
        """
        Load data from a file and initialize related attributes.

        Args:
            sampling_rate (float): Sampling rate of the data in Hz.
        """
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.data, self.time = load_data(file_path)
            self.sampling_rate = sampling_rate
            self.time = self.time / self.sampling_rate
            self.channel_mapping = list(range(self.data.shape[1]))
            self.selected_channels = self.channel_mapping.copy()
            self.update_channel_statistics()
            self.update_callback()

    def update_channel_statistics(self):
        """
        Update the channel statistics if data is available.
        """
        if self.data is not None:
            self.channel_statistics = compute_channel_statistics(self.data)
        else:
            self.channel_statistics = None

    def update_peak_statistics(self):
        """
        Update the peak statistics if peaks are detected.
        """
        if self.peaks is not None and self.sampling_rate is not None:
            self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time, self.sampling_rate)

    def save_statistics_to_excel(self):
        """
        Save channel and peak statistics to an Excel file.
        """
        if self.channel_statistics is None:
            messagebox.showwarning("Warning", "No statistics available to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path) as writer:
                channel_df = pd.DataFrame(self.channel_statistics)
                channel_df['Original Channel'] = self.channel_mapping
                channel_df = channel_df.set_index('Original Channel')
                channel_df.to_excel(writer, sheet_name='Channel Statistics')

                if self.peak_statistics:
                    peak_df = pd.DataFrame(self.peak_statistics)
                    peak_df['Original Channel'] = self.channel_mapping
                    peak_df = peak_df.set_index('Original Channel')
                    peak_df.to_excel(writer, sheet_name='Peak Statistics')
                else:
                    messagebox.showwarning("Warning", "No peak statistics available. Only channel statistics will be saved.")

            messagebox.showinfo("Success", f"Statistics saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def get_data(self):
        """
        Get a dictionary containing all the data and related information.

        Returns:
            dict: A dictionary containing data, time, artifacts, peaks, peak windows,
                  average peak windows, channel mapping, and selected channels.
        """
        return {
            'data': self.data,
            'time': self.time,
            'artifacts': self.artifacts,
            'peaks': self.peaks,
            'peak_windows': self.peak_windows,
            'avg_peak_windows': self.avg_peak_windows,
            'channel_mapping': self.channel_mapping,
            'selected_channels': self.selected_channels
        }

    def trim_data(self, start_idx, end_idx):
        """
        Trim the data and update related attributes.

        Args:
            start_idx (int): Starting index for trimming.
            end_idx (int): Ending index for trimming.
        """
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
            self.avg_peak_windows = [np.mean(windows, axis=0) if len(windows) > 0 else None for windows in self.peak_windows]
        else:
            self.avg_peak_windows = None

        self.update_channel_statistics()
        self.update_peak_statistics()
        self.update_callback()

    def delete_channels(self, channels_to_delete):
        """
        Delete specified channels and update related attributes.

        Args:
            channels_to_delete (list): List of channel indices to delete.
        """
        channels_to_delete = sorted(channels_to_delete, reverse=True)
        for channel in channels_to_delete:
            index = self.channel_mapping.index(channel)
            self.data = np.delete(self.data, index, axis=1)
            if self.artifacts is not None:
                self.artifacts = np.delete(self.artifacts, index, axis=1)
            if self.peaks is not None:
                del self.peaks[index]
            if self.peak_windows is not None:
                del self.peak_windows[index]
            if self.avg_peak_windows is not None:
                del self.avg_peak_windows[index]
            del self.channel_mapping[index]

        self.selected_channels = [ch for ch in self.selected_channels if ch not in channels_to_delete]
        self.update_channel_statistics()
        self.update_peak_statistics()
        self.update_callback()

    def keep_channels(self, channels_to_keep):
        """
        Keep only specified channels and delete the rest.

        Args:
            channels_to_keep (list): List of channel indices to keep.
        """
        channels_to_delete = [ch for ch in self.channel_mapping if ch not in channels_to_keep]
        self.delete_channels(channels_to_delete)

    def save_comprehensive_peak_data(self):
        """
        Save comprehensive peak data to a CSV file.
        This includes peak times, amplitudes, and inter-peak distances for each channel.
        """
        if self.peaks is None or self.data is None:
            messagebox.showwarning("Warning", "No peak data available. Please detect peaks first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'w') as f:
                f.write("Channel, Peak Time (s),Peak Amplitude (mV),Inter-Peak Distance (s)\n")
                for channel, peaks in enumerate(self.peaks):
                    peak_times = self.time[peaks]
                    peak_amplitudes = self.data[peaks, channel]
                    inter_peak_distances = np.diff(peak_times)
                    
                    for i, (time, amplitude) in enumerate(zip(peak_times, peak_amplitudes)):
                        if i == 0:
                            f.write(f"{self.channel_mapping[channel]},{time:.6f},{amplitude:.6f},\n")
                        else:
                            f.write(f"{self.channel_mapping[channel]},{time:.6f},{amplitude:.6f},{inter_peak_distances[i-1]:.6f}\n")
            messagebox.showinfo("Success", f"Comprehensive peak data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def save_peak_windows(self):
        """
        Save all peak windows to a CSV file.
        Each row represents a peak window, with columns for channel number, peak number, and voltage values.
        """
        if self.peak_windows is None or self.data is None:
            messagebox.showwarning("Warning", "No peak window data available. Please detect peaks first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                header = ['Channel', 'Peak Number'] + [f'V{i}' for i in range(len(self.peak_windows[0][0]))]
                writer.writerow(header)

                for channel, channel_windows in enumerate(self.peak_windows):
                    for peak_number, window in enumerate(channel_windows):
                        row = [self.channel_mapping[channel], peak_number] + list(window)
                        writer.writerow(row)

            messagebox.showinfo("Success", f"Peak windows saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def clear_all_data(self):
        """Clear all data and statistics."""
        self.data = None
        self.time = None
        self.sampling_rate = None
        self.artifacts = None
        self.peaks = None
        self.peak_windows = None
        self.avg_peak_windows = None
        self.channel_mapping = []
        self.channel_statistics = None
        self.peak_statistics = None
        self.selected_channels = []
        self.update_callback()