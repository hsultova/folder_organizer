import shutil
import re

from datetime import datetime
from pathlib import Path

from categories import category_for
from history import log_move, undo_last_operations
from utils import unique_path

OLD_FILES_DAYS = 30  # Number of days to consider a file as old

def organize_folder(folder: str, add_date: bool = True, move_old_files: bool = False, undo: bool = False) -> None:
    """
    Organize files in the specified folder based on their extensions. 
    Optionally, add the date to the filename and move old files to a separate folder.
    :param folder: The path to the folder to organize.
    :param add_date: Whether to add the date to the filename (default is True).
    :param move_old_files: Whether to move old files to a separate folder (default is False).
    :param undo: Whether to undo the last file organization operation (default is False).
    """
    folder_path = Path(folder)
    if not folder_path.exists():    
        print(f"The folder '{folder}' does not exist.")
        return

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") 
    if undo:
        undo_last_operations()
        return

    for file in folder_path.iterdir():
        if not file.is_file():
            continue

        category = category_for(file.suffix.lower())

        if move_old_files and is_file_old(file):
            target_folder = folder_path / "Old_Files" / category
        else:
            target_folder = folder_path / category

        try:
            move_file(run_id, file, target_folder, add_date)
        except OSError as err:
            print(f"Could not move {file.name}: {err}")

def move_file(run_id: str, file: Path, folder_to_move: Path, add_date: bool) -> None:
    """Move a file to the specified folder. If the folder does not exist, create it.
    Optionally, add the date to the filename.
    """  
    folder_to_move.mkdir(parents=True, exist_ok=True)
    file_name = file.name    
    file_to_move = folder_to_move / file_name
    if add_date:
        regex = r'\d{2,4}[-._]\d{2}[-._]\d{2,4}'
        if re.search(regex, file_name):
            print(f"File '{file_name}' already has a date in its name. Skipping date addition.")
        else:
            date = datetime.fromtimestamp(file.stat().st_mtime).date()
            print(f"Renamed '{file_name}' to '{f'{date}_{file.name}'}'")
            file_name = f"{date}_{file.name}"
            file_to_move = folder_to_move / file_name

    unique_file_to_move = unique_path(file_to_move)
    if unique_file_to_move != file_to_move:
        print(f"File '{file_name}' already exists. Renamed to '{unique_file_to_move.name}'")
        file_name = unique_file_to_move.name
        file_to_move = unique_file_to_move

    shutil.move(file, file_to_move)
    print(f"Moved '{file_name}' to '{folder_to_move}'\n")
    log_move(run_id, file, file_to_move)

def is_file_old(file: Path) -> bool:
    """Check if a file is older than 30 days based on its last modified time.
    """
    cutoff_date = datetime.now().timestamp() - (OLD_FILES_DAYS * 86400)  # OLD_FILES_DAYS days in seconds
    return file.stat().st_mtime < cutoff_date