import tkinter as tk
from tkinter import ttk

class StatisticsPanel(ttk.Frame):
    """
    A panel for displaying statistics about channels and peaks in the electrophysiology data.
    
    This panel is a child of ttk.Frame and creates a tabbed interface to show channel and peak statistics.
    """

    def __init__(self, parent):
        """
        Initialize the StatisticsPanel.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, style="Dark.TFrame", width=350)  # Set width to 350 pixels
        self.pack_propagate(False)  # Prevent the frame from shrinking to fit its contents
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all widgets within the StatisticsPanel."""
        # Create and pack the title label
        self.title_label = ttk.Label(self, text="Statistics", style="Dark.TLabel", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 20))

        # Create a notebook (tabbed interface) for channel and peak statistics
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and add the Channel Statistics tab
        self.channel_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.channel_frame, text="Channel Stats")

        # Create and add the Peak Statistics tab
        self.peak_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.peak_frame, text="Peak Stats")

        # Create Treeviews for each tab
        self.channel_tree = self.create_treeview(self.channel_frame, ["Channel", "Mean (mV)", "Std Dev (mV)"])
        self.peak_tree = self.create_treeview(self.peak_frame, [
            "Channel", "Peaks", "Frequency (Hz)", "Avg Amplitude (mV)", "Std Amplitude (mV)",
            "Mean Inter-Peak Distance (samples)", "Std Inter-Peak Distance (samples)",
            "Mean Inter-Peak Time (ms)", "Std Inter-Peak Time (ms)"
        ])

    def create_treeview(self, parent, columns):
        """
        Create a Treeview widget with scrollbars.

        Args:
            parent: The parent widget for the Treeview.
            columns: A list of column names for the Treeview.

        Returns:
            ttk.Treeview: The created Treeview widget.
        """
        # Create a frame to hold the Treeview and scrollbars
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create horizontal and vertical scrollbars
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical")

        # Create the Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show="headings", style="Dark.Treeview",
                            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Configure scrollbars
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)

        # Grid layout for Treeview and scrollbars
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Configure column headings and widths
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)  # Set column width to 120 pixels

        return tree

    def update_statistics(self, channel_statistics=None, peak_statistics=None, channel_mapping=None):
        """
        Update the statistics displayed in the Treeviews.

        Args:
            channel_statistics (list): A list of dictionaries containing channel statistics.
            peak_statistics (list): A list of dictionaries containing peak statistics.
            channel_mapping (dict): A dictionary mapping channel indices to their original numbers.
        """
        if channel_statistics and channel_mapping:
            # Clear existing items in the channel statistics Treeview
            self.channel_tree.delete(*self.channel_tree.get_children())
            # Insert new channel statistics
            for stats in channel_statistics:
                original_channel = channel_mapping[stats['channel']]
                self.channel_tree.insert("", "end", values=(
                    original_channel,
                    f"{stats['mean']:.2f}",
                    f"{stats['std']:.2f}"
                ))

        if peak_statistics and channel_mapping:
            # Clear existing items in the peak statistics Treeview
            self.peak_tree.delete(*self.peak_tree.get_children())
            # Insert new peak statistics
            for stats in peak_statistics:
                original_channel = channel_mapping[stats['channel']]
                self.peak_tree.insert("", "end", values=(
                    original_channel,
                    stats['num_peaks'],
                    f"{stats['frequency']:.2f}",
                    f"{stats['avg_amplitude']:.2f}",
                    f"{stats['std_amplitude']:.2f}",
                    f"{stats['mean_inter_peak_distance']:.2f}",
                    f"{stats['std_inter_peak_distance']:.2f}",
                    f"{stats['mean_inter_peak_time']*1000:.2f}",  # Convert to ms
                    f"{stats['std_inter_peak_time']*1000:.2f}"    # Convert to ms
                ))

    def clear_statistics(self):
        """Clear all statistics from the Treeviews."""
        self.channel_tree.delete(*self.channel_tree.get_children())
        self.peak_tree.delete(*self.peak_tree.get_children())