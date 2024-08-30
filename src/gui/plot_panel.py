import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

class PlotPanel(ttk.Frame):
    """
    Panel for displaying interactive data visualizations using Plotly.

    This class creates and manages the plots for displaying the electrophysiological data,
    including the main plot and the peak plot. It handles the plot styling and interactive features.

    Attributes:
        main_plot (go.Figure): The main Plotly Figure object.
        peak_plot (go.Figure): The Plotly Figure object for the peak plot.
        main_html (HTMLScrolledText): The HTML widget for displaying the main plot.
        peak_html (HTMLScrolledText): The HTML widget for displaying the peak plot.
    """

    def __init__(self, parent):
        """
        Initialize the PlotPanel.

        Args:
            parent (tk.Widget): The parent widget for this panel.
        """
        super().__init__(parent, style="Plot.TFrame")

        self.main_figure, (self.main_ax) = plt.subplots(figsize=(10, 6), dpi=100)
        self.peak_figure, (self.peak_ax) = plt.subplots(figsize=(10, 3), dpi=100)

        self.main_canvas = FigureCanvasTkAgg(self.main_figure, master=self)
        self.main_canvas.draw()
        self.main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.main_canvas, self)
        self.toolbar.update()
        self.main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.peak_canvas = FigureCanvasTkAgg(self.peak_figure, master=self)
        self.peak_canvas.draw()
        self.peak_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.configure(style="Plot.TFrame")

        self.create_peak_view_buttons()
        self.peak_view_mode = "average"
        self.current_data = None

    def create_peak_view_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        avg_button = ttk.Button(button_frame, text="Average Peak", command=lambda: self.set_peak_view_mode("average"))
        avg_button.pack(side=tk.LEFT, padx=5, pady=5)

        all_button = ttk.Button(button_frame, text="All Peaks", command=lambda: self.set_peak_view_mode("all"))
        all_button.pack(side=tk.LEFT, padx=5, pady=5)

        all_avg_button = ttk.Button(button_frame, text="All Peaks with Average", command=lambda: self.set_peak_view_mode("all_with_average"))
        all_avg_button.pack(side=tk.LEFT, padx=5, pady=5)

    def set_peak_view_mode(self, mode):
        self.peak_view_mode = mode
        if self.current_data is not None:
            self.update_plot(self.current_data)

    def update_plot(self, data=None):
        """
        Update the main plot with new data.

        Args:
            data (dict): Dictionary containing the data, time, artifacts, peaks, peak windows, and selected channels.
        """
        if data is None:
            return

        self.current_data = data
        self.main_ax.clear()
        self.peak_ax.clear()

        for i in data['selected_channels']:
            channel_data = data['data'][:, i]
            time = data['time']
            artifacts = data['artifacts'][:, i] if data['artifacts'] is not None else None
            peaks = data['peaks'][i] if data['peaks'] is not None and i < len(data['peaks']) else None
            peak_windows = data['peak_windows'][i] if data['peak_windows'] is not None and i < len(data['peak_windows']) else None
            avg_peak_window = data['avg_peak_windows'][i] if data['avg_peak_windows'] is not None and i < len(data['avg_peak_windows']) else None

            self.main_ax.plot(time, channel_data, label=f"Channel {i+1}")
            
            if artifacts is not None:
                self.main_ax.scatter(time[artifacts], channel_data[artifacts], color='red', s=20, label=f"Artifacts Ch{i+1}")
            
            if peaks is not None:
                self.main_ax.scatter(time[peaks], channel_data[peaks], color='green', marker='x', s=50, label=f"Peaks Ch{i+1}")

            if peak_windows is not None and avg_peak_window is not None:
                self.update_peak_plot(peak_windows, avg_peak_window, i)

        self.style_plot(self.main_ax, "Time (s)", "Voltage (uV)")
        self.style_plot(self.peak_ax, "Time (samples)", "Voltage (uV)")

        self.main_canvas.draw()
        self.peak_canvas.draw()

    def update_peak_plot(self, peak_windows, avg_peak_window, channel):
        """
        Update the peak plot with new peak windows.

        Args:
            peak_windows (list): List of arrays containing peak windows for each channel.
            avg_peak_window (array): Average peak window for the channel.
            channel (int): Channel number.
        """
        if peak_windows is None or len(peak_windows) == 0 or avg_peak_window is None:
            return

        time = np.arange(avg_peak_window.shape[0])
        
        if self.peak_view_mode == "average" or self.peak_view_mode == "all_with_average":
            self.peak_ax.plot(time, avg_peak_window, 'r-', linewidth=2, label=f"Average Peak Ch{channel+1}")

        if self.peak_view_mode == "all" or self.peak_view_mode == "all_with_average":
            for i, window in enumerate(peak_windows):
                self.peak_ax.plot(time, window, 'b-', alpha=0.3, label=f"Peak {i+1} Ch{channel+1}" if i == 0 else "")

    def style_plot(self, ax, x_label, y_label):
        """
        Apply consistent styling to a plot.

        Args:
            ax (matplotlib.axes.Axes): The matplotlib Axes object to style.
            x_label (str): Label for x-axis.
            y_label (str): Label for y-axis.
        """
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend(facecolor='black', edgecolor='white', labelcolor='white')

        # Set the figure background to black
        ax.figure.patch.set_facecolor('black')