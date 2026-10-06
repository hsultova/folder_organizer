import shutil
import os

from datetime import datetime
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

# Organize files in the specified folder based on their extensions. Optionally, 
# add the date to the filename and move old files to a separate folder.
def organize_folder(folder: str, add_date: bool = True, move_old_files: bool = False) -> None:
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
                    if move_old_files and is_file_old(file):
                        category_path = folder_path / 'Old_Files' / category
                    move_file(file, category_path, add_date)
                    is_moved = True
                    break

            if not is_moved:
                others_path = folder_path / 'Others'
                move_file(file, others_path, add_date)

# Move a file to the specified folder. If the folder does not exist, create it.
# Optionally, add the date to the filename.
def move_file(file: Path, folder_to_move: Path, add_date: bool = True) -> None:
    if not folder_to_move.exists():
        os.makedirs(folder_to_move)
    file_name = file.name    
    file_to_move = folder_to_move / file_name
    if(add_date):
        date = datetime.fromtimestamp(file.stat().st_mtime).date()
        print(f"Renamed '{file_name}' to '{f"{date}_{file.name}"}'")
        file_name = f"{date}_{file.name}"
        file_to_move = folder_to_move / file_name

    shutil.move(file, file_to_move)
    print(f"Moved '{file_name}' to '{folder_to_move}'\n")

# Check if a file is older than 30 days
def is_file_old(file: Path) -> bool:
    cutoff_date = datetime.now().timestamp() - (30 * 86400)  # 30 days in seconds
    return file.stat().st_mtime < cutoff_date
