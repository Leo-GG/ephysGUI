import customtkinter as ctk
from .control_panel import ControlPanel

class ElectrophysiologyAnalyzer(ctk.CTk):
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

        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu_frame = ctk.CTkFrame(self)
        menu_frame.pack(side="top", fill="x")

        file_button = ctk.CTkButton(menu_frame, text="File", command=self.show_file_menu)
        file_button.pack(side="left", padx=5, pady=5)

        help_button = ctk.CTkButton(menu_frame, text="Help", command=self.show_help_menu)
        help_button.pack(side="left", padx=5, pady=5)

    def show_file_menu(self):
        file_menu = ctk.CTkToplevel(self)
        file_menu.geometry("200x250")
        file_menu.title("File Menu")

        load_button = ctk.CTkButton(file_menu, text="Load Data", command=self.load_data)
        load_button.pack(pady=5, padx=10, fill="x")

        save_stats_button = ctk.CTkButton(file_menu, text="Save Statistics", command=self.save_statistics)
        save_stats_button.pack(pady=5, padx=10, fill="x")

        save_peak_data_button = ctk.CTkButton(file_menu, text="Save Peak Data", command=self.save_comprehensive_peak_data)
        save_peak_data_button.pack(pady=5, padx=10, fill="x")

        save_peak_windows_button = ctk.CTkButton(file_menu, text="Save Peak Waveforms", command=self.save_peak_windows)
        save_peak_windows_button.pack(pady=5, padx=10, fill="x")

        clear_data_button = ctk.CTkButton(file_menu, text="Clear All Data", command=self.clear_all_data)
        clear_data_button.pack(pady=5, padx=10, fill="x")

        exit_button = ctk.CTkButton(file_menu, text="Exit", command=self.quit)
        exit_button.pack(pady=5, padx=10, fill="x")

    def show_help_menu(self):
        help_menu = ctk.CTkToplevel(self)
        help_menu.geometry("200x100")
        help_menu.title("Help Menu")

        about_button = ctk.CTkButton(help_menu, text="About", command=self.show_about)
        about_button.pack(pady=5, padx=10, fill="x")

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        self.control_panel = ControlPanel(main_frame)
        self.control_panel.pack(side="left", fill="y")

    def load_data(self):
        self.control_panel.load_data()

    def save_statistics(self):
        self.control_panel.save_statistics_to_excel()

    def save_comprehensive_peak_data(self):
        self.control_panel.save_comprehensive_peak_data()

    def save_peak_windows(self):
        self.control_panel.save_peak_windows()

    def clear_all_data(self):
        self.control_panel.clear_all_data()

    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("400x300")

        about_text = """
        Electrophysiology Data Analysis Tool

        Version: 0.1
        
        This program is designed to analyze electrophysiological data,
        including filtering, artifact detection, and peak analysis.

        Created by: Leonardo Garma
        August 2024
        
        leonardogarma@gmail.com
        """
        
        label = ctk.CTkLabel(about_window, text=about_text, wraplength=380, justify="left")
        label.pack(padx=10, pady=10)

if __name__ == "__main__":
    app = ElectrophysiologyAnalyzer()
    app.mainloop()