import tkinter as tk
from tkinter import ttk

class StatisticsPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Dark.TFrame", width=250)
        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Peak Statistics", style="Dark.TLabel", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 20))

        self.stats_text = tk.Text(self, wrap=tk.WORD, bg="#1E1E1E", fg="white", font=("Arial", 12))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.stats_text.config(state=tk.DISABLED)

    def update_statistics(self, statistics):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        for stats in statistics:
            self.stats_text.insert(tk.END, f"Channel {stats['channel']}:\n")
            self.stats_text.insert(tk.END, f"  Peaks: {stats['num_peaks']}\n")
            self.stats_text.insert(tk.END, f"  Frequency: {stats['frequency']:.2f} Hz\n")
            self.stats_text.insert(tk.END, f"  Avg Amplitude: {stats['avg_amplitude']:.2f} mV\n")
            self.stats_text.insert(tk.END, f"  Std Amplitude: {stats['std_amplitude']:.2f} mV\n\n")
        
        self.stats_text.config(state=tk.DISABLED)