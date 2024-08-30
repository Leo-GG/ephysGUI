import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import SpanSelector
import numpy as np

class PlotPanel(ttk.Frame):
    def __init__(self, parent, trim_callback):
        super().__init__(parent)
        self.trim_callback = trim_callback
        self.fig, self.canvas = self.create_plot()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add the matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure toolbar style
        self.toolbar.config(background='black')
        self.toolbar._message_label.config(background='black', foreground='white')
        for button in self.toolbar.winfo_children():
            if isinstance(button, tk.Button):
                button.config(background='#333333', foreground='white')

        self.span_selector = None
        self.selected_range = None
        self.span_selector_active = False

    def create_plot(self):
        fig = plt.figure(figsize=(10, 8), dpi=100, facecolor='black')
        canvas = FigureCanvasTkAgg(fig, master=self)
        
        # Create subplots with fixed positions
        self.ax1 = fig.add_axes([0.1, 0.55, 0.8, 0.35])  # [left, bottom, width, height]
        self.ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.35])
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('black')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
        
        self.ax1.set_title("Electrophysiology Data", fontsize=14, fontweight='bold', color='white')
        self.ax1.set_xlabel("Time (s)", fontsize=12, color='white')
        self.ax1.set_ylabel("Voltage (mV)", fontsize=12, color='white')
        
        self.ax2.set_title("Average Peak Window", fontsize=14, fontweight='bold', color='white')
        self.ax2.set_xlabel("Time (ms)", fontsize=12, color='white')
        self.ax2.set_ylabel("Voltage (mV)", fontsize=12, color='white')
        
        return fig, canvas

    def update_plot(self, data_dict):
        self.ax1.clear()
        self.ax2.clear()
        
        self.ax1.set_facecolor('black')
        self.ax2.set_facecolor('black')
        
        self.ax1.set_title("Electrophysiology Data", fontsize=14, fontweight='bold', color='white')
        self.ax1.set_xlabel("Time (s)", fontsize=12, color='white')
        self.ax1.set_ylabel("Voltage (mV)", fontsize=12, color='white')
        
        self.ax2.set_title("Average Peak Window", fontsize=14, fontweight='bold', color='white')
        self.ax2.set_xlabel("Time (ms)", fontsize=12, color='white')
        self.ax2.set_ylabel("Voltage (mV)", fontsize=12, color='white')
        
        if data_dict['data'] is not None:
            selected_channels = data_dict['selected_channels']
            for i, channel_index in enumerate(selected_channels):
                self.ax1.plot(data_dict['time'], data_dict['data'][:, i], label=f'Channel {channel_index+1}')
            
            if data_dict['artifacts'] is not None:
                for i, channel_index in enumerate(selected_channels):
                    artifact_mask = data_dict['artifacts'][:, i]
                    self.ax1.plot(data_dict['time'][artifact_mask], data_dict['data'][artifact_mask, i], 'rx')
            
            if data_dict['peaks'] is not None:
                for i, channel_index in enumerate(selected_channels):
                    channel_peaks = data_dict['peaks'][i]
                    self.ax1.plot(data_dict['time'][channel_peaks], data_dict['data'][channel_peaks, i], 'go')
            
            if data_dict['avg_peak_windows'] is not None:
                for i, channel_index in enumerate(selected_channels):
                    avg_window = data_dict['avg_peak_windows'][i]
                    if avg_window is not None:
                        window_time = np.linspace(-50, 50, len(avg_window))
                        self.ax2.plot(window_time, avg_window, label=f'Channel {channel_index+1}')
        
        for ax in [self.ax1, self.ax2]:
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.legend(fontsize=10, facecolor='black', edgecolor='white', labelcolor='white')
        
        self.canvas.draw()
        self.toolbar.update()

        # Create or update span selector based on its active state
        if self.span_selector_active:
            self.create_span_selector()
        else:
            self.remove_span_selector()

    def create_span_selector(self):
        if self.span_selector is None:
            self.span_selector = SpanSelector(
                self.ax1, self.on_select, 'horizontal', useblit=True,
                props=dict(alpha=0.5, facecolor='red'),
                interactive=True, drag_from_anywhere=True
            )
        self.span_selector.set_visible(True)

    def remove_span_selector(self):
        if self.span_selector is not None:
            self.span_selector.set_visible(False)
        self.selected_range = None

    def on_select(self, xmin, xmax):
        self.selected_range = (xmin, xmax)
        self.trim_callback(self.selected_range)

    def toggle_span_selector(self):
        self.span_selector_active = not self.span_selector_active
        if self.span_selector_active:
            self.create_span_selector()
        else:
            self.remove_span_selector()
        self.canvas.draw()