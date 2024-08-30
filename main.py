import customtkinter as ctk
from src.gui.analyzer_gui import ElectrophysiologyAnalyzer

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ElectrophysiologyAnalyzer()
    app.mainloop()