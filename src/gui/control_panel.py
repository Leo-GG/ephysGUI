import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.data_handling.data_loader import load_data
from src.analysis.signal_processing import apply_notch_filter, apply_lowpass_filter, apply_highpass_filter, detect_peaks, extract_peak_windows
from src.analysis.artifact_detection import detect_artifacts_all_channels
import numpy as np

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

    def __init__(self, parent, update_callback):
        """
        Initialize the ControlPanel.

        Args:
            parent (tk.Widget): The parent widget for this panel.
            update_callback (function): Callback function to update the plot.
        """
        super().__init__(parent, style="Left.TFrame", width=250)
        self.pack_propagate(False)
        self.update_callback = update_callback

        self.data = None
        self.time = None
        self.sampling_rate = None
        self.artifacts = None
        self.peaks = None
        self.peak_windows = None
        self.avg_peak_windows = None

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the control widgets."""
        self.configure(style="Left.TFrame")
        self.create_load_button()
        self.create_filter_options()
        self.create_channel_selection()

    def create_load_button(self):
        """Create the 'Load Data' button."""
        load_button = ttk.Button(self, text="Load Data", command=self.load_data, style="TButton")
        load_button.pack(fill=tk.X, pady=(0, 20))

    def create_filter_options(self):
        """Create widgets for filter options, artifact detection, and peak detection."""
        filter_frame = ttk.Frame(self, style="Filter.TFrame")
        filter_frame.pack(fill=tk.X, pady=(0, 20))

        # Sampling rate
        sr_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        sr_frame.pack(fill=tk.X, pady=5)
        sr_label = ttk.Label(sr_frame, text="Sampling Rate (Hz):", style="Text.TLabel")
        sr_label.pack(side=tk.LEFT)
        self.sr_entry = ttk.Entry(sr_frame, width=10, style="Dark.TEntry")
        self.sr_entry.pack(side=tk.RIGHT)
        self.sr_entry.insert(0, "20000")

        # Notch filter
        notch_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        notch_frame.pack(fill=tk.X, pady=5)
        notch_label = ttk.Label(notch_frame, text="Notch Filter (Hz):", style="Text.TLabel")
        notch_label.pack(side=tk.LEFT)
        self.notch_entry = ttk.Entry(notch_frame, width=10, style="Dark.TEntry")
        self.notch_entry.pack(side=tk.RIGHT)
        self.notch_entry.insert(0, "50")
        notch_button = ttk.Button(filter_frame, text="Apply Notch", command=lambda: self.apply_filter('notch'), style="TButton")
        notch_button.pack(fill=tk.X, pady=5)

        # Low-pass filter
        lowpass_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        lowpass_frame.pack(fill=tk.X, pady=5)
        lowpass_label = ttk.Label(lowpass_frame, text="Low-pass Filter (Hz):", style="Text.TLabel")
        lowpass_label.pack(side=tk.LEFT)
        self.lowpass_entry = ttk.Entry(lowpass_frame, width=10, style="Dark.TEntry")
        self.lowpass_entry.pack(side=tk.RIGHT)
        self.lowpass_entry.insert(0, "100")
        lowpass_button = ttk.Button(filter_frame, text="Apply Low-pass", command=lambda: self.apply_filter('lowpass'), style="TButton")
        lowpass_button.pack(fill=tk.X, pady=5)

        # High-pass filter
        highpass_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        highpass_frame.pack(fill=tk.X, pady=5)
        highpass_label = ttk.Label(highpass_frame, text="High-pass Filter (Hz):", style="Text.TLabel")
        highpass_label.pack(side=tk.LEFT)
        self.highpass_entry = ttk.Entry(highpass_frame, width=10, style="Dark.TEntry")
        self.highpass_entry.pack(side=tk.RIGHT)
        self.highpass_entry.insert(0, "1")
        highpass_button = ttk.Button(filter_frame, text="Apply High-pass", command=lambda: self.apply_filter('highpass'), style="TButton")
        highpass_button.pack(fill=tk.X, pady=5)

        # Artifact detection
        artifact_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        artifact_frame.pack(fill=tk.X, pady=5)
        artifact_label = ttk.Label(artifact_frame, text="Artifact Threshold:", style="Text.TLabel")
        artifact_label.pack(side=tk.LEFT)
        self.artifact_entry = ttk.Entry(artifact_frame, width=10, style="Dark.TEntry")
        self.artifact_entry.pack(side=tk.RIGHT)
        self.artifact_entry.insert(0, "5")
        artifact_button = ttk.Button(filter_frame, text="Detect Artifacts", command=self.detect_artifacts, style="TButton")
        artifact_button.pack(fill=tk.X, pady=5)

        # Peak detection
        peak_frame = ttk.Frame(filter_frame, style="Filter.TFrame")
        peak_frame.pack(fill=tk.X, pady=5)
        peak_label = ttk.Label(peak_frame, text="Peak Threshold:", style="Text.TLabel")
        peak_label.pack(side=tk.LEFT)
        self.peak_entry = ttk.Entry(peak_frame, width=10, style="Dark.TEntry")
        self.peak_entry.pack(side=tk.RIGHT)
        self.peak_entry.insert(0, "50")  # Changed default value to 50
        peak_button = ttk.Button(filter_frame, text="Detect Peaks", command=self.detect_peaks, style="TButton")
        peak_button.pack(fill=tk.X, pady=5)

    def create_channel_selection(self):
        """Create the channel selection listbox."""
        channel_frame = ttk.Frame(self, style="Channel.TFrame")
        channel_frame.pack(fill=tk.BOTH, expand=True)

        channel_label = ttk.Label(channel_frame, text="Channels", style="Header.TLabel")
        channel_label.pack(pady=(0, 10))

        self.channel_listbox = tk.Listbox(channel_frame, selectmode=tk.MULTIPLE, bg="#1E1E1E", fg="white", font=("Arial", 10))
        self.channel_listbox.pack(fill=tk.BOTH, expand=True)
        self.channel_listbox.bind("<<ListboxSelect>>", lambda e: self.update_callback())

    def load_data(self):
        """Load data from a file and update the channel list."""
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.data, self.time = load_data(file_path)
            self.sampling_rate = float(self.sr_entry.get())
            self.update_channel_list()
            self.update_callback()

    def update_channel_list(self):
        """Update the channel listbox with the available channels."""
        self.channel_listbox.delete(0, tk.END)
        for i in range(self.data.shape[1]):
            self.channel_listbox.insert(tk.END, f"Channel {i+1}")

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
            window_size = 2000  # Define window size
            
            # Print debug information
            print(f"Threshold: {threshold}")
            print(f"Data shape: {self.data.shape}")
            print(f"Sampling rate: {self.sampling_rate}")
            
            self.peaks = []
            self.peak_windows = []
            self.avg_peak_windows = []
            
            for channel in range(self.data.shape[1]):
                channel_data = self.data[:, channel]
                channel_peaks = detect_peaks(channel_data, 
                                             distance=int(self.sampling_rate * 0.5),  # Assume minimum 0.5s between peaks
                                             threshold=threshold,
                                             window_size=window_size)
                
                self.peaks.append(channel_peaks)
                
                channel_peak_windows = extract_peak_windows(channel_data, channel_peaks, window_size=window_size)
                self.peak_windows.append(channel_peak_windows)
                
                if len(channel_peak_windows) > 0:
                    self.avg_peak_windows.append(np.mean(channel_peak_windows, axis=0))
                else:
                    self.avg_peak_windows.append(None)
            
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
            'selected_channels': self.get_selected_channels()
        }

    def get_selected_channels(self):
        """
        Get the indices of the selected channels.

        Returns:
            list: List of indices of the selected channels.
        """
        return [i for i in self.channel_listbox.curselection()]