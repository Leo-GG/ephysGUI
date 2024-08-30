import tkinter as tk
from tkinter import ttk, messagebox
from src.analysis.signal_processing import apply_notch_filter, apply_lowpass_filter, apply_highpass_filter, detect_peaks, extract_peak_windows
from src.analysis.artifact_detection import detect_artifacts_all_channels
import numpy as np

class FilterPanel(ttk.Frame):
    def __init__(self, parent, data_manager, update_callback):
        super().__init__(parent, style="Dark.TFrame")
        self.data_manager = data_manager
        self.update_callback = update_callback
        self.create_widgets()

    def create_widgets(self):
        # Sampling rate
        sr_frame = ttk.Frame(self, style="Dark.TFrame")
        sr_frame.pack(fill=tk.X, pady=5)
        sr_label = ttk.Label(sr_frame, text="Sampling Rate (Hz):", style="Dark.TLabel")
        sr_label.pack(side=tk.LEFT)
        self.sr_entry = ttk.Entry(sr_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.sr_entry.pack(side=tk.RIGHT)
        self.sr_entry.insert(0, "20000")

        # Notch filter
        notch_frame = ttk.Frame(self, style="Dark.TFrame")
        notch_frame.pack(fill=tk.X, pady=5)
        notch_label = ttk.Label(notch_frame, text="Notch Filter (Hz):", style="Dark.TLabel")
        notch_label.pack(side=tk.LEFT)
        self.notch_entry = ttk.Entry(notch_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.notch_entry.pack(side=tk.RIGHT)
        self.notch_entry.insert(0, "50")
        notch_button = ttk.Button(self, text="Apply Notch", command=lambda: self.apply_filter('notch'), style="Dark.TButton")
        notch_button.pack(fill=tk.X, pady=5)

        # Low-pass filter
        lowpass_frame = ttk.Frame(self, style="Dark.TFrame")
        lowpass_frame.pack(fill=tk.X, pady=5)
        lowpass_label = ttk.Label(lowpass_frame, text="Low-pass Filter (Hz):", style="Dark.TLabel")
        lowpass_label.pack(side=tk.LEFT)
        self.lowpass_entry = ttk.Entry(lowpass_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.lowpass_entry.pack(side=tk.RIGHT)
        self.lowpass_entry.insert(0, "100")
        lowpass_button = ttk.Button(self, text="Apply Low-pass", command=lambda: self.apply_filter('lowpass'), style="Dark.TButton")
        lowpass_button.pack(fill=tk.X, pady=5)

        # High-pass filter
        highpass_frame = ttk.Frame(self, style="Dark.TFrame")
        highpass_frame.pack(fill=tk.X, pady=5)
        highpass_label = ttk.Label(highpass_frame, text="High-pass Filter (Hz):", style="Dark.TLabel")
        highpass_label.pack(side=tk.LEFT)
        self.highpass_entry = ttk.Entry(highpass_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.highpass_entry.pack(side=tk.RIGHT)
        self.highpass_entry.insert(0, "1")
        highpass_button = ttk.Button(self, text="Apply High-pass", command=lambda: self.apply_filter('highpass'), style="Dark.TButton")
        highpass_button.pack(fill=tk.X, pady=5)

        # Artifact detection
        artifact_frame = ttk.Frame(self, style="Dark.TFrame")
        artifact_frame.pack(fill=tk.X, pady=5)
        artifact_label = ttk.Label(artifact_frame, text="Artifact Threshold:", style="Dark.TLabel")
        artifact_label.pack(side=tk.LEFT)
        self.artifact_entry = ttk.Entry(artifact_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.artifact_entry.pack(side=tk.RIGHT)
        self.artifact_entry.insert(0, "5")
        artifact_button = ttk.Button(self, text="Detect Artifacts", command=self.detect_artifacts, style="Dark.TButton")
        artifact_button.pack(fill=tk.X, pady=5)

        # Peak detection
        peak_frame = ttk.Frame(self, style="Dark.TFrame")
        peak_frame.pack(fill=tk.X, pady=5)
        peak_label = ttk.Label(peak_frame, text="Peak Threshold:", style="Dark.TLabel")
        peak_label.pack(side=tk.LEFT)
        self.peak_entry = ttk.Entry(peak_frame, width=10, style="Dark.TEntry", font=("Arial", 14))
        self.peak_entry.pack(side=tk.RIGHT)
        self.peak_entry.insert(0, "50")

        # Add checkbox for peak polarity
        self.peak_polarity_var = tk.BooleanVar(value=False)
        self.peak_polarity_check = ttk.Checkbutton(
            self,
            text="Detect Positive Peaks",
            variable=self.peak_polarity_var,
            style="Dark.TCheckbutton"
        )
        self.peak_polarity_check.pack(fill=tk.X, pady=5)

        peak_button = ttk.Button(self, text="Detect Peaks", command=self.detect_peaks, style="Dark.TButton")
        peak_button.pack(fill=tk.X, pady=5)

    def apply_filter(self, filter_type):
        if self.data_manager.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            if filter_type == 'notch':
                freq = float(self.notch_entry.get())
                self.data_manager.data = apply_notch_filter(self.data_manager.data, self.data_manager.sampling_rate, freq)
            elif filter_type == 'lowpass':
                freq = float(self.lowpass_entry.get())
                self.data_manager.data = apply_lowpass_filter(self.data_manager.data, self.data_manager.sampling_rate, freq)
            elif filter_type == 'highpass':
                freq = float(self.highpass_entry.get())
                self.data_manager.data = apply_highpass_filter(self.data_manager.data, self.data_manager.sampling_rate, freq)
            self.update_callback()
        except ValueError:
            messagebox.showerror("Error", f"Invalid {filter_type} frequency.")

    def detect_artifacts(self):
        if self.data_manager.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            threshold = float(self.artifact_entry.get())
            self.data_manager.artifacts = detect_artifacts_all_channels(self.data_manager.data, threshold=threshold)
            self.update_callback()
        except ValueError:
            messagebox.showerror("Error", "Invalid artifact threshold.")

    def detect_peaks(self):
        if self.data_manager.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            threshold = float(self.peak_entry.get())
            window_size = int(self.data_manager.sampling_rate * 0.1)  # 100ms window
            detect_positive = self.peak_polarity_var.get()
            
            print(f"Threshold: {threshold}")
            print(f"Data shape: {self.data_manager.data.shape}")
            print(f"Sampling rate: {self.data_manager.sampling_rate}")
            print(f"Detecting {'positive' if detect_positive else 'negative'} peaks")
            
            self.data_manager.peaks = []
            self.data_manager.peak_windows = []
            self.data_manager.avg_peak_windows = []
            
            for channel in range(self.data_manager.data.shape[1]):
                channel_data = self.data_manager.data[:, channel]
                channel_peaks = detect_peaks(channel_data, self.data_manager.sampling_rate, threshold, 
                                             detect_positive=detect_positive, window_size=window_size)
                
                self.data_manager.peaks.append(channel_peaks)
                
                channel_peak_windows = extract_peak_windows(channel_data, channel_peaks, window_size)
                self.data_manager.peak_windows.append(channel_peak_windows)
                
                if len(channel_peak_windows) > 0:
                    self.data_manager.avg_peak_windows.append(np.mean(channel_peak_windows, axis=0))
                else:
                    self.data_manager.avg_peak_windows.append(None)
            
            self.data_manager.update_peak_statistics()
            self.update_callback()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during peak detection: {str(e)}")

    def get_sampling_rate(self):
        return float(self.sr_entry.get())