import tkinter as tk
from tkinter import ttk

def create_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Helvetica', 12), borderwidth=1, background='#4a4a4a', foreground='white')
    style.configure('TLabel', font=('Helvetica', 12), background='#2b2b2b', foreground='white')
    style.configure('TLabelframe', font=('Helvetica', 14, 'bold'), background='#2b2b2b', foreground='white')
    style.configure('TLabelframe.Label', font=('Helvetica', 14, 'bold'), background='#2b2b2b', foreground='white')
    style.configure('TEntry', font=('Helvetica', 12), fieldbackground='#3c3c3c', foreground='white')
    style.configure('TCombobox', font=('Helvetica', 12), fieldbackground='#3c3c3c', foreground='white')
    return style


def create_file_section(master, load_data_command):
    file_frame = ttk.Frame(master, padding="10", style='TFrame')
    load_button = ttk.Button(file_frame, text="Load Data", command=load_data_command)
    load_button.pack(side="left")
    return file_frame, load_button

def create_channel_section(master, plot_data_command):
    channel_frame = ttk.Frame(master, padding="10", style='TFrame')
    channel_var = tk.StringVar(value="All")
    channel_label = ttk.Label(channel_frame, text="Select Channel:")
    channel_menu = ttk.Combobox(channel_frame, textvariable=channel_var, state="readonly")
    channel_menu.bind("<<ComboboxSelected>>", lambda _: plot_data_command())
    
    channel_label.pack(side="left", padx=(0, 5))
    channel_menu.pack(side="left", expand=True, fill="x")
    
    return channel_frame, channel_var, channel_label, channel_menu

def create_artifact_section(master, run_artifact_detection_command):
    artifact_frame = ttk.LabelFrame(master, text="Artifact Detection", padding="10", style='TLabelframe')
    artifact_threshold_label = ttk.Label(artifact_frame, text="Threshold:")
    artifact_threshold = ttk.Entry(artifact_frame, width=10)
    artifact_threshold.insert(0, "3")
    artifact_button = ttk.Button(artifact_frame, text="Run Artifact Detection", command=run_artifact_detection_command)
    
    artifact_threshold_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    artifact_threshold.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    artifact_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    return artifact_frame, artifact_threshold, artifact_button

def create_peak_section(master, run_peak_detection_command):
    peak_frame = ttk.LabelFrame(master, text="Peak Detection", padding="10", style='TLabelframe')
    peak_height_label = ttk.Label(peak_frame, text="Height:")
    peak_height = ttk.Entry(peak_frame, width=10)
    peak_height.insert(0, "1")
    peak_distance_label = ttk.Label(peak_frame, text="Distance:")
    peak_distance = ttk.Entry(peak_frame, width=10)
    peak_distance.insert(0, "50")
    peak_button = ttk.Button(peak_frame, text="Run Peak Detection", command=run_peak_detection_command)
    
    peak_height_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    peak_height.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    peak_distance_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    peak_distance.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    peak_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="e")
    
    return peak_frame, peak_height, peak_distance, peak_button