import tkinter as tk
from tkinter import ttk, messagebox
from .control_panel import ControlPanel

class ElectrophysiologyAnalyzer(tk.Tk):
    """
    Main application window for the Electrophysiology Data Analyzer.

    This class sets up the main GUI window, including the control panel
    and the plot panel. It manages the overall layout and styling of the
    application.

    Attributes:
        control_panel (ControlPanel): Panel for user inputs and controls.
        plot_panel (PlotPanel): Panel for data visualization.
    """

    def __init__(self):
        """
        Initialize the main window and set up the GUI components.

        This method creates the main window, sets its size and title,
        and initializes the control and plot panels.
        """
        super().__init__()

        self.title("Electrophysiology Data Analysis Tool")
        self.geometry("1400x800")
        self.configure(bg="#000000")

        self.create_styles()
        self.create_menu()
        self.create_widgets()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Dark.TFrame", background="#000000")
        self.style.configure("Dark.TButton", background="#333333", foreground="white", font=("Arial", 12))
        self.style.map("Dark.TButton",
                       background=[('active', '#4A6984')],
                       foreground=[('active', 'white')])
        self.style.configure("Dark.TLabel", background="#000000", foreground="white", font=("Arial", 12))
        self.style.configure("Dark.TEntry", fieldbackground="#333333", foreground="white", font=("Arial", 14))
        self.style.configure("Dark.TCheckbutton", background="#000000", foreground="white", font=("Arial", 12))
        
        # Configure Treeview style
        self.style.configure("Dark.Treeview",
                             background="#1E1E1E",
                             foreground="white",
                             fieldbackground="#1E1E1E",
                             font=("Arial", 12))
        self.style.configure("Dark.Treeview.Heading",
                             background="#333333",
                             foreground="white",
                             font=("Arial", 12, "bold"))
        self.style.map("Dark.Treeview", background=[('selected', '#4A6984')])

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_command(label="Save Statistics", command=self.save_statistics)
        file_menu.add_command(label="Save Peak Data", command=self.save_comprehensive_peak_data)
        file_menu.add_command(label="Save Peak Waveforms", command=self.save_peak_windows)
        file_menu.add_separator()
        file_menu.add_command(label="Clear All Data", command=self.clear_all_data)  # Add this line
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        """
        Create and arrange the main GUI components.

        This method creates the main frame, initializes the control panel
        and plot panel, and arranges them within the main window.
        """
        main_frame = ttk.Frame(self, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the control panel
        self.control_panel = ControlPanel(main_frame)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        # The PlotPanel and StatisticsPanel are now created inside the ControlPanel

        # Adjust the window size to accommodate the wider StatisticsPanel
        self.geometry("1400x800")  # Increased width from 1200 to 1400

    def load_data(self):
        """
        Open a file dialog to select and load data files.
        """
        file_types = [
            ('All supported files', '*.npy;*.rhd'),
            ('NumPy files', '*.npy'),
            ('Intan RHD files', '*.rhd'),
            ('All files', '*.*')
        ]
        self.control_panel.load_data(filetypes=file_types)

    def save_statistics(self):
        self.control_panel.save_statistics_to_excel()

    def save_comprehensive_peak_data(self):
        self.control_panel.save_comprehensive_peak_data()

    def save_peak_windows(self):
        self.control_panel.save_peak_windows()

    def clear_all_data(self):
        self.control_panel.clear_all_data()

    def show_about(self):
        about_text = """
        Electrophysiology Data Analysis Tool

        Version: 0.1
        
        This program is designed to analyze electrophysiological data,
        including filtering, artifact detection, and peak analysis.

        Created by: Leonardo Garma
        August 2024
        
        leonardogarma@gmail.com
        """
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    app = ElectrophysiologyAnalyzer()
    app.mainloop()