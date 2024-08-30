import numpy as np
from tkinter import filedialog, messagebox
from src.data_handling.data_loader import load_data
from src.analysis.peak_statistics import compute_channel_statistics, compute_peak_statistics
import pandas as pd

class DataManager:
    def __init__(self, update_callback):
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
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.data, self.time = load_data(file_path)
            self.sampling_rate = sampling_rate
            self.time = self.time / self.sampling_rate
            self.channel_mapping = list(range(self.data.shape[1]))
            self.selected_channels = self.channel_mapping.copy()  # Initialize selected channels
            self.update_channel_statistics()  # Compute channel statistics immediately after loading
            self.update_callback()

    def update_channel_statistics(self):
        if self.data is not None:
            self.channel_statistics = compute_channel_statistics(self.data)
        else:
            self.channel_statistics = None

    def update_peak_statistics(self):
        if self.peaks is not None:
            self.peak_statistics = compute_peak_statistics(self.data, self.peaks, self.time)

    def save_statistics_to_excel(self):
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
        channels_to_delete = [ch for ch in self.channel_mapping if ch not in channels_to_keep]
        self.delete_channels(channels_to_delete)