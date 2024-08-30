import tkinter as tk
from tkinter import ttk
from .plot_panel import PlotPanel
from .control_panel import ControlPanel

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Electrophysiology Data Analyzer")
        self.geometry("1400x800")
        self.configure(bg="#000000")

        self.create_widgets()
        self.style_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.control_panel = ControlPanel(main_frame, self.update_plot)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        self.plot_panel = PlotPanel(main_frame)
        self.plot_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def style_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Set consistent background color
        bg_color = "#000000"
        fg_color = "white"
        
        style.configure("Main.TFrame", background=bg_color)
        style.configure("Left.TFrame", background=bg_color)
        style.configure("Plot.TFrame", background=bg_color)
        style.configure("Filter.TFrame", background=bg_color)
        style.configure("Channel.TFrame", background=bg_color)
        
        style.configure("TButton", 
                        background="#1E1E1E",
                        foreground=fg_color,
                        padding=10)
        style.map("TButton",
                  background=[("active", "#2E2E2E")])
        
        style.configure("Header.TLabel", 
                        background=bg_color, 
                        foreground=fg_color, 
                        font=("Arial", 14, "bold"))
        
        style.configure("Text.TLabel", 
                        background=bg_color, 
                        foreground=fg_color)
        
        style.configure("Dark.TEntry", 
                        fieldbackground="#1E1E1E", 
                        foreground=fg_color, 
                        insertcolor=fg_color)

    def update_plot(self):
        self.plot_panel.update_plot(self.control_panel.get_data())