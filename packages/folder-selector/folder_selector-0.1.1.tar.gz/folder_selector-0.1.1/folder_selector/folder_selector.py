import tkinter as tk
from tkinter import filedialog, messagebox
import json
import threading

class FolderSelectorApp:
    def __init__(self, root, default_folder="/path/to/default/folder", folder_list=None, completion_event=None):
        self.root = root
        self.root.title("Multiple Folder Selector")
        
        self.default_folder = default_folder  # Set default folder path
        self.folder_list = folder_list if folder_list is not None else []
        self.checkbuttons = []
        self.completion_event = completion_event

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

        self.select_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)
        
        self.folder_frame = tk.Frame(root)
        self.folder_frame.pack(pady=10)
        
        self.clear_button = tk.Button(root, text="Clear Selection", command=self.clear_selection)
        self.clear_button.pack(pady=10)
        
        self.save_button = tk.Button(root, text="Save List", command=self.save_list)
        self.save_button.pack(pady=10)
        
        self.load_button = tk.Button(root, text="Load List", command=self.load_list)
        self.load_button.pack(pady=10)
        
        self.done_button = tk.Button(root, text="Done", command=self.done)
        self.done_button.pack(pady=10)
        
    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.default_folder, mustexist=True)
        if folder and folder not in self.folder_list:
            self.folder_list.append(folder)
            self.add_checkbutton(folder)
        
    def add_checkbutton(self, folder):
        var = tk.BooleanVar()
        checkbutton = tk.Checkbutton(self.folder_frame, text=folder, variable=var)
        checkbutton.pack(anchor='w')
        self.checkbuttons.append((checkbutton, var))
        
    def clear_selection(self):
        self.folder_list = []
        for checkbutton, var in self.checkbuttons:
            checkbutton.destroy()
        self.checkbuttons = []
        
    def save_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.folder_list, file)
                messagebox.showinfo("Save Successful", "The folder list has been saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the folder list: {e}")
                
    def load_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.folder_list = json.load(file)
                self.update_checkbuttons()
                messagebox.showinfo("Load Successful", "The folder list has been loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading the folder list: {e}")
                
    def update_checkbuttons(self):
        # Clear current checkbuttons
        for checkbutton, var in self.checkbuttons:
            checkbutton.destroy()
        self.checkbuttons = []
        
        # Add checkbuttons for loaded folders
        for folder in self.folder_list:
            self.add_checkbutton(folder)
            
    def done(self):
        if self.completion_event:
            self.completion_event.set()
        self.root.destroy()

    def on_closing(self):
        if self.completion_event:
            self.completion_event.set()
        self.root.destroy()
        
def start_folder_selector(default_folder, folder_list, completion_event):
    root = tk.Tk()
    app = FolderSelectorApp(root, default_folder=default_folder, folder_list=folder_list, completion_event=completion_event)
    root.mainloop()

def select_folders(default_folder="/path/to/default/folder"):
    folder_list = []
    completion_event = threading.Event()
    
    # Start the folder selector in a separate thread
    thread = threading.Thread(target=start_folder_selector, args=(default_folder, folder_list, completion_event))
    thread.start()
    
    # Wait until the folder selection is complete or the window is closed
    completion_event.wait()
    
    return folder_list
