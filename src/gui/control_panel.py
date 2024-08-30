import customtkinter as ctk
from .plot_panel import PlotPanel
from .statistics_panel import StatisticsPanel
from .data_manager import DataManager
from .filter_panel import FilterPanel
from .channel_panel import ChannelPanel

class ControlPanel(ctk.CTkFrame):
    """
    A panel that controls the main functionality of the Electrophysiology Data Analyzer.

    This panel contains various widgets for data loading, processing, and visualization control.
    It also manages interactions between different components of the application.

    Attributes:
        data_manager (DataManager): Manages the electrophysiology data and related operations.
        plot_panel (PlotPanel): Handles the visualization of the data.
        statistics_panel (StatisticsPanel): Displays statistical information about the data.
        filter_panel (FilterPanel): Contains controls for applying filters to the data.
        channel_panel (ChannelPanel): Manages channel selection and related operations.
    """

    def __init__(self, parent):
        """
        Initialize the ControlPanel.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, width=250)
        self.pack_propagate(False)

        self.data_manager = DataManager(self.update_callback)
        
        self.plot_panel = PlotPanel(parent, self.update_trim_button)
        self.plot_panel.pack(side="right", fill="both", expand=True)
        
        self.statistics_panel = StatisticsPanel(parent)
        self.statistics_panel.pack(side="right", fill="y")

        self.filter_panel = FilterPanel(self, self.data_manager, self.update_callback)
        self.filter_panel.pack(fill="x", pady=10)

        self.channel_panel = ChannelPanel(self, self.data_manager, self.update_callback)
        self.channel_panel.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        """Create and configure the widgets for the ControlPanel."""
        self.toggle_span_button = ctk.CTkButton(self, text="Toggle Span Selector", command=self.toggle_span_selector, corner_radius=10)
        self.toggle_span_button.pack(fill="x", pady=5)

        self.trim_button = ctk.CTkButton(self, text="Trim Data", command=self.trim_data, state="disabled", corner_radius=10)
        self.trim_button.pack(fill="x", pady=5)

    def load_data(self):
        """Load data using the current sampling rate and update the UI."""
        sampling_rate = self.filter_panel.get_sampling_rate()
        self.data_manager.load_data(sampling_rate)
        self.channel_panel.update_channel_list()
        self.update_callback()

    def save_statistics_to_excel(self):
        """Save the current channel statistics to an Excel file."""
        if self.data_manager.channel_statistics is None:
            messagebox.showwarning("Warning", "No channel statistics available. Please load data first.")
            return
        self.data_manager.save_statistics_to_excel()

    def toggle_span_selector(self):
        """Toggle the span selector on the plot panel."""
        self.plot_panel.toggle_span_selector()
        if self.plot_panel.span_selector_active:
            self.toggle_span_button.config(text="Disable Span Selector")
        else:
            self.toggle_span_button.config(text="Enable Span Selector")

    def update_trim_button(self, selected_range):
        """
        Update the state of the trim button based on the selected range.

        Args:
            selected_range (tuple): The selected range (min, max) or None if no range is selected.
        """
        self.selected_range = selected_range
        self.trim_button.config(state=tk.NORMAL if selected_range is not None else tk.DISABLED)

    def trim_data(self):
        """Trim the data based on the selected range in the plot."""
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
        """
        Update the plot and statistics panels with the current data.

        Args:
            event: Optional event data (not used).
        """
        data_dict = self.data_manager.get_data()
        self.plot_panel.update_plot(data_dict)
        self.statistics_panel.update_statistics(
            channel_statistics=self.data_manager.channel_statistics,
            peak_statistics=self.data_manager.peak_statistics,
            channel_mapping=self.data_manager.channel_mapping
        )

    def save_comprehensive_peak_data(self):
        """Save comprehensive peak data to a CSV file."""
        if self.data_manager.peaks is None:
            messagebox.showwarning("Warning", "No peak data available. Please detect peaks first.")
            return
        self.data_manager.save_comprehensive_peak_data()

    def save_peak_windows(self):
        """Save all peak windows to a CSV file."""
        if self.data_manager.peak_windows is None:
            messagebox.showwarning("Warning", "No peak window data available. Please detect peaks first.")
            return
        self.data_manager.save_peak_windows()

    def clear_all_data(self):
        """Clear all data and statistics after user confirmation."""
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data and statistics? This action cannot be undone.")
        if confirm:
            self.data_manager.clear_all_data()
            self.channel_panel.update_channel_list()
            self.statistics_panel.clear_statistics()
            messagebox.showinfo("Info", "All data and statistics have been cleared.")
