import tkinter as tk
from tkinter import ttk

class StatisticsPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Dark.TFrame", width=350)  # Increased width
        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Statistics", style="Dark.TLabel", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 20))

        # Create a notebook for channel and peak statistics
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Channel Statistics Tab
        self.channel_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.channel_frame, text="Channel Stats")

        # Peak Statistics Tab
        self.peak_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.peak_frame, text="Peak Stats")

        # Create Treeviews for each tab
        self.channel_tree = self.create_treeview(self.channel_frame, ["Channel", "Mean (mV)", "Std Dev (mV)"])
        self.peak_tree = self.create_treeview(self.peak_frame, ["Channel", "Peaks", "Frequency (Hz)", "Avg Amplitude (mV)", "Std Amplitude (mV)"])

    def create_treeview(self, parent, columns):
        # Create a frame to hold the Treeview and scrollbars
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create horizontal and vertical scrollbars
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical")

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
            tree.column(col, anchor="center", width=120)  # Increased column width

        return tree

    def update_statistics(self, channel_statistics=None, peak_statistics=None, channel_mapping=None):
        if channel_statistics and channel_mapping:
            self.channel_tree.delete(*self.channel_tree.get_children())
            for stats in channel_statistics:
                original_channel = channel_mapping[stats['channel']]  # Remove the -1
                self.channel_tree.insert("", "end", values=(
                    original_channel,
                    f"{stats['mean']:.2f}",
                    f"{stats['std']:.2f}"
                ))

        if peak_statistics and channel_mapping:
            self.peak_tree.delete(*self.peak_tree.get_children())
            for stats in peak_statistics:
                original_channel = channel_mapping[stats['channel']]  # Remove the -1
                self.peak_tree.insert("", "end", values=(
                    original_channel,
                    stats['num_peaks'],
                    f"{stats['frequency']:.2f}",
                    f"{stats['avg_amplitude']:.2f}",
                    f"{stats['std_amplitude']:.2f}"
                ))