import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class PlotPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Plot.TFrame")
        self.create_widgets()

    def create_widgets(self):
        self.configure(style="Plot.TFrame")  # Set the background color for the entire panel
        self.create_main_plot()
        self.create_peak_plot()

    def create_main_plot(self):
        main_plot_frame = ttk.Frame(self, style="Plot.TFrame")
        main_plot_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        main_plot_label = ttk.Label(main_plot_frame, text="Data Visualization", style="Header.TLabel")
        main_plot_label.pack(pady=(0, 10))

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor("#000000")
        self.plot = self.figure.add_subplot(111)
        self.style_plot(self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure, main_plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Remove white stripes
        #self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
        self.figure.subplots_adjust( bottom=0.2)

    def create_peak_plot(self):
        peak_plot_frame = ttk.Frame(self, style="Plot.TFrame")
        peak_plot_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        peak_plot_label = ttk.Label(peak_plot_frame, text="Average Peak Windows", style="Header.TLabel")
        peak_plot_label.pack(pady=(0, 10))

        self.peak_figure = Figure(figsize=(5, 3), dpi=100)
        self.peak_figure.patch.set_facecolor("#000000")
        self.peak_plot = self.peak_figure.add_subplot(111)
        self.style_plot(self.peak_plot)
        self.peak_canvas = FigureCanvasTkAgg(self.peak_figure, peak_plot_frame)
        self.peak_canvas.draw()
        self.peak_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Remove white stripes
        #self.peak_figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
        self.peak_figure.subplots_adjust(bottom=0.2)

    def style_plot(self, plot):
        plot.set_facecolor("#000000")
        plot.spines['bottom'].set_visible(True)
        plot.spines['left'].set_visible(True)
        plot.spines['bottom'].set_color('white')
        plot.spines['left'].set_color('white')
        plot.tick_params(axis='x', colors='white')
        plot.tick_params(axis='y', colors='white')

    def update_plot(self, data):
        if data['data'] is None:
            return

        self.plot.clear()
        self.style_plot(self.plot)

        for channel in data['selected_channels']:
            self.plot.plot(data['time'], data['data'][:, channel], label=f"Channel {channel+1}")
            
            if data['artifacts'] is not None:
                artifact_mask = data['artifacts'][:, channel]
                self.plot.scatter(data['time'][artifact_mask], data['data'][artifact_mask, channel], 
                                  color='red', s=10, label=f"Artifacts Ch{channel+1}")
            
            if data['peaks'] is not None:
                channel_peaks = data['peaks'][channel]
                self.plot.scatter(data['time'][channel_peaks], data['data'][channel_peaks, channel],
                                  color='green', s=50, marker='x', label=f"Peaks Ch{channel+1}")

        self.plot.set_xlabel("Samples", color="white")
        self.plot.set_ylabel("Voltage", color="white")
        self.plot.legend(facecolor="#000000", edgecolor="none", fontsize=8, labelcolor="white")
        self.canvas.draw()

        self.update_peak_plot(data)

    def update_peak_plot(self, data):
        if data['peak_windows'] is None:
            return

        self.peak_plot.clear()
        self.style_plot(self.peak_plot)

        for channel in data['selected_channels']:
            windows = data['peak_windows'][channel]
            if len(windows) == 0:
                continue

            mean_window = np.mean(windows, axis=0)
            std_window = np.std(windows, axis=0)
            x = np.arange(len(mean_window))

            self.peak_plot.plot(x, mean_window, label=f"Channel {channel+1}")
            self.peak_plot.fill_between(x, mean_window - std_window, mean_window + std_window, alpha=0.3)

        #self.peak_plot.set_title("Average Peak Windows", color='white')
        self.peak_plot.set_xlabel("Samples", color='white')
        self.peak_plot.set_ylabel("Voltage", color='white')
        self.peak_plot.legend(facecolor="#000000", edgecolor="none", fontsize=8, labelcolor="white")
        self.peak_canvas.draw()