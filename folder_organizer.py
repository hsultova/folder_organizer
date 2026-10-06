import shutil

from pathlib import Path

# Define the file types and their corresponding extensions
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.ipynb'],
    'Others': []
}

# Organize files in the specified folder
def organize_folder(folder: str):
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"The folder '{folder}' does not exist.")
        return

    for file in folder_path.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            is_moved = False

            for category, extensions in file_types.items():
                if file_extension in extensions:
                    category_path = folder_path / category                    
                    move_file(file, category_path)
                    is_moved = True
                    break

            if not is_moved:
                others_path = folder_path / 'Others'
                move_file(file, others_path)

# Move a file to the specified folder. If the folder does not exist, create it.
def move_file(file, folder_to_move):
    if not folder_to_move.exists():
        folder_to_move.mkdir()

    shutil.move(file, folder_to_move / file.name)
    print(f"Moved '{file.name}' to '{folder_to_move}'")
