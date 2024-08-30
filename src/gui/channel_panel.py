import tkinter as tk
from tkinter import ttk, messagebox

class ChannelPanel(ttk.Frame):
    def __init__(self, parent, data_manager, update_callback):
        super().__init__(parent, style="Dark.TFrame")
        self.data_manager = data_manager
        self.update_callback = update_callback
        self.select_all_state = False
        self.create_widgets()

    def create_widgets(self):
        channel_label = ttk.Label(self, text="Channels", style="Dark.TLabel")
        channel_label.pack(pady=(0, 10))

        self.channel_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, bg="#1E1E1E", fg="white", font=("Arial", 12))
        self.channel_listbox.pack(fill=tk.BOTH, expand=True)
        self.channel_listbox.bind("<<ListboxSelect>>", self.on_select)

        # Add Select/Unselect All button
        self.select_all_button = ttk.Button(self, text="Select All", command=self.toggle_select_all, style="Dark.TButton")
        self.select_all_button.pack(fill=tk.X, pady=5)

        # Add Delete Channel button
        self.delete_channel_button = ttk.Button(self, text="Delete Selected Channels", command=self.delete_selected_channels, style="Dark.TButton")
        self.delete_channel_button.pack(fill=tk.X, pady=5)

        # Add Keep Selected Channels button
        self.keep_selected_button = ttk.Button(self, text="Keep Only Selected Channels", command=self.keep_selected_channels, style="Dark.TButton")
        self.keep_selected_button.pack(fill=tk.X, pady=5)

    def update_channel_list(self):
        self.channel_listbox.delete(0, tk.END)
        for original_channel in self.data_manager.channel_mapping:
            self.channel_listbox.insert(tk.END, f"Channel {original_channel}")
        # Select only the first channel by default
        self.channel_listbox.select_set(0)
        self.on_select(None)
        self.select_all_state = False
        self.select_all_button.config(text="Select All")

    def on_select(self, event):
        selected_indices = self.channel_listbox.curselection()
        self.data_manager.selected_channels = [self.data_manager.channel_mapping[i] for i in selected_indices]
        self.update_callback()

    def toggle_select_all(self):
        if self.select_all_state:
            self.channel_listbox.selection_clear(0, tk.END)
            self.select_all_button.config(text="Select All")
        else:
            self.channel_listbox.select_set(0, tk.END)
            self.select_all_button.config(text="Unselect All")
        self.select_all_state = not self.select_all_state
        self.on_select(None)

    def get_selected_channels(self):
        return self.data_manager.selected_channels

    def delete_selected_channels(self):
        selected_indices = self.channel_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one channel to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected channels? This action cannot be undone.")
        if confirm:
            channels_to_delete = [self.data_manager.channel_mapping[i] for i in selected_indices]
            self.data_manager.delete_channels(channels_to_delete)
            self.update_channel_list()

    def keep_selected_channels(self):
        selected_indices = self.channel_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one channel to keep.")
            return

        confirm = messagebox.askyesno("Confirm Keep", "Are you sure you want to keep only the selected channels? This action cannot be undone.")
        if confirm:
            channels_to_keep = [self.data_manager.channel_mapping[i] for i in selected_indices]
            self.data_manager.keep_channels(channels_to_keep)
            self.update_channel_list()