import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog
import logging

EXTENSIONS_DICT = {
    '.txt': 'Documents',
    '.docx': 'Documents',
    '.pdf': 'Documents',
    '.jpg': 'Images',
    '.png': 'Images',
    '.exe': 'Executables',
    '.py': 'Python',
    '.mp3': 'Audio',
    '.mp4': 'Videos',
    '.xlsx': 'Spreadsheets',
    '.zip': 'Compressed',
    '.html': 'Web',
}

DEFAULT_CATEGORY = 'Others'

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        self.target_folder_path = tk.StringVar()
        self.status_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Select a folder to organize").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.browse_button = ttk.Button(self.root, text="Browse", command=self.browse_button_click)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def browse_button_click(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_folder_path.set(folder_selected)
            self.organize_files(folder_selected)

    def organize_files(self, target_folder):
        try:
            logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            files_processed = 0
            total_files = 0

            for root_folder, _, files in os.walk(target_folder):
                total_files += len(files)

            self.progress_bar["maximum"] = total_files

            for root_folder, _, files in os.walk(target_folder):
                for file in files:
                    source_file_path = os.path.join(root_folder, file)
                    if os.path.isfile(source_file_path):
                        _, extension = os.path.splitext(file)
                        category = EXTENSIONS_DICT.get(extension.lower(), DEFAULT_CATEGORY)
                        target_folder_path = os.path.join(target_folder, category)
                        if not os.path.exists(target_folder_path):
                            os.makedirs(target_folder_path)

                        target_file_path = os.path.join(target_folder_path, file)
                        if os.path.exists(target_file_path):
                            logging.warning(f"File '{file}' already exists in '{target_folder_path}'. Renaming...")
                            base_name, extension = os.path.splitext(file)
                            renamed_file = base_name + "_renamed" + extension
                            target_file_path = os.path.join(target_folder_path, renamed_file)
                            logging.info(f"Renamed file to '{renamed_file}'")

                        shutil.move(source_file_path, target_file_path)
                        logging.info(f"Moved '{file}' to '{target_folder_path}'")

                        files_processed += 1
                        self.progress_bar["value"] = files_processed
                        self.root.update_idletasks()

            self.update_status("File organization completed.", "green")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")

    def update_status(self, message, color):
        self.status_var.set(message)
        self.status_label.config(foreground=color)

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.geometry("400x200")
    root.mainloop()

if __name__ == "__main__":
    main()
