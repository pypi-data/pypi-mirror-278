from folder_selector import select_folders

def main():
    print("Starting folder selection...")
    selected_folders = select_folders(default_folder="/path/to/your/default/folder")
    print("Folder selection completed.")
    print("Selected folders:", selected_folders)

if __name__ == "__main__":
    main()
