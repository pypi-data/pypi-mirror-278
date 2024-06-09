import threading
from folder_selector import start_folder_selector

def main():
    folder_list = []
    completion_event = threading.Event()
    
    # Run the folder selector in a separate thread
    thread = threading.Thread(target=start_folder_selector, args=("/path/to/your/default/folder", folder_list, completion_event))
    thread.start()
    
    # Wait until the folder selection is complete
    print("Waiting for folder selection to complete...")
    completion_event.wait()
    print("Folder selection completed.")
    
    # Now you can access the selected folders
    print("Selected folders:", folder_list)
    
if __name__ == "__main__":
    main()
