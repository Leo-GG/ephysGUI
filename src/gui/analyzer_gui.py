import tkinter as tk
from tkinter import ttk
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

        self.title("Electrophysiology Data Analyzer")
        self.geometry("1200x800")
        self.configure(bg="#000000")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Dark.TFrame", background="#000000")
        self.style.configure("Dark.TButton", background="#333333", foreground="white", font=("Arial", 12))
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

        self.create_widgets()

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

if __name__ == "__main__":
    app = ElectrophysiologyAnalyzer()
    app.mainloop()