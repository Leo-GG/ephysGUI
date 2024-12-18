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
        self.configure(bg="#2E2E2E")

        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange the main GUI components.

        This method creates the main frame, initializes the control panel
        and plot panel, and arranges them within the main window.
        """
        main_frame = ttk.Frame(self, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the control panel
        self.control_panel = ControlPanel(main_frame)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        # The PlotPanel is now created inside the ControlPanel

    def update_plot(self):
        # This method is no longer needed as the PlotPanel updates itself
        pass

if __name__ == "__main__":
    app = ElectrophysiologyAnalyzer()
    app.mainloop()