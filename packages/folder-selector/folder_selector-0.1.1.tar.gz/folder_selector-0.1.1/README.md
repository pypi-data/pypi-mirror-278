# Folder Selector

A Tkinter-based folder selector for Python applications.

## Installation

```bash
pip install folder_selector

## Usage

Basic Example
To use the folder_selector library, you can call the select_folders function. This function will open a GUI for selecting folders and return the list of selected folders once the user is done.

Here's a basic example:

python
Copia codice
from folder_selector import select_folders

def main():
    print("Starting folder selection...")
    selected_folders = select_folders(default_folder="/path/to/your/default/folder")
    print("Folder selection completed.")
    print("Selected folders:", selected_folders)

if __name__ == "__main__":
    main()
    
Parameters
default_folder (optional): The initial folder path to start browsing from. Defaults to "/path/to/default/folder" if not specified.