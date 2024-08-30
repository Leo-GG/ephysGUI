import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PlotPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.fig, self.canvas = self.create_plot()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_plot(self):
        fig = plt.figure(figsize=(10, 8), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self)
        
        # Create subplots with fixed positions
        self.ax1 = fig.add_axes([0.1, 0.55, 0.8, 0.35])  # [left, bottom, width, height]
        self.ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.35])
        
        self.ax1.set_title("Electrophysiology Data", fontsize=12, fontweight='bold')
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Voltage (mV)")
        
        self.ax2.set_title("Average Peak Window", fontsize=12, fontweight='bold')
        self.ax2.set_xlabel("Time (ms)")
        self.ax2.set_ylabel("Voltage (mV)")
        
        return fig, canvas

    def update_plot(self, data_dict):
        self.ax1.clear()
        self.ax2.clear()
        
        self.ax1.set_title("Electrophysiology Data", fontsize=12, fontweight='bold')
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Voltage (mV)")
        
        self.ax2.set_title("Average Peak Window", fontsize=12, fontweight='bold')
        self.ax2.set_xlabel("Time (ms)")
        self.ax2.set_ylabel("Voltage (mV)")
        
        if data_dict['data'] is not None:
            selected_channels = data_dict['selected_channels']
            for i in selected_channels:
                self.ax1.plot(data_dict['time'], data_dict['data'][:, i], label=f'Channel {i+1}')
            
            if data_dict['artifacts'] is not None:
                for i in selected_channels:
                    artifact_mask = data_dict['artifacts'][:, i]
                    self.ax1.plot(data_dict['time'][artifact_mask], data_dict['data'][artifact_mask, i], 'rx')
            
            if data_dict['peaks'] is not None:
                for i, channel_peaks in enumerate(data_dict['peaks']):
                    if i in selected_channels:
                        self.ax1.plot(data_dict['time'][channel_peaks], data_dict['data'][channel_peaks, i], 'go')
            
            if data_dict['avg_peak_windows'] is not None:
                for i, avg_window in enumerate(data_dict['avg_peak_windows']):
                    if i in selected_channels and avg_window is not None:
                        window_time = np.linspace(-50, 50, len(avg_window))
                        self.ax2.plot(window_time, avg_window, label=f'Channel {i+1}')
        
        self.ax1.legend()
        self.ax2.legend()
        
        self.canvas.draw()