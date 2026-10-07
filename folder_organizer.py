import shutil
import re

from datetime import datetime
from pathlib import Path

from categories import category_for
from history import log_move, undo_last_run
from utils import next_available_path

DATE_IN_NAME_PATTERN = re.compile(r"\d{2,4}[-._]\d{2}[-._]\d{2,4}")
OLD_FILE_AGE_DAYS = 30  # Number of days to consider a file as old

def organize_folder(folder: str, add_date: bool = True, move_old_files: bool = False, undo: bool = False) -> list[str]:
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
        undo_last_run()
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

def dated_name(file: Path) -> str:
    """Return the file's name prefixed with its last modified date.
    Names that already contain a date are returned unchanged.
    """
    if DATE_IN_NAME_PATTERN.search(file.name):
        print(f"File '{file.name}' already has a date in its name. Skipping date addition.")
        return file.name

    date = datetime.fromtimestamp(file.stat().st_mtime).date()
    new_name = f"{date}_{file.name}"
    print(f"Renamed '{file.name}' to '{new_name}'")
    return new_name

def move_file(run_id: str, file: Path, destination_folder: Path, add_date: bool) -> None:
    """Move a file into the specified folder, creating the folder if it does not exist.
    Optionally, add the date to the filename.
    """
    destination_folder.mkdir(parents=True, exist_ok=True)

    file_name = dated_name(file) if add_date else file.name
    destination = next_available_path(destination_folder / file_name)
    if destination.name != file_name:
        print(f"File '{file_name}' already exists. Renamed to '{destination.name}'")

    shutil.move(file, destination)
    log_move(run_id, file, destination)
    print(f"File '{file.name}' moved to '{destination}'")

def is_file_old(file: Path) -> bool:
    f"""Check if a file is older than the specified number of days - {OLD_FILE_AGE_DAYS}.
    """
    cutoff_date = datetime.now().timestamp() - (OLD_FILE_AGE_DAYS * 86400)  # OLD_FILE_AGE_DAYS days in seconds
    return file.stat().st_mtime < cutoff_date
