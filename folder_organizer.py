import shutil
import csv
import re

from datetime import datetime
from pathlib import Path

# Define the file types and their corresponding extensions
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.ipynb'],
}

OLD_FILES_DAYS = 30  # Number of days to consider a file as old

LOG_FILE = Path(__file__).parent / "file_log.csv"
LOG_COLUMNS = ["run_id", "timestamp", "source", "destination"]

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

def category_for(extension: str) -> str:
    """Return the category folder name for a file extension."""
    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category
    return "Others"

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


def unique_path(target: Path) -> Path:
    """
    Generate a unique file path by appending a counter to the filename if the target path already exists.
    """
    if not target.exists():
        return target
    counter = 1
    while True:
        candidate = target.with_name(f"{target.stem} ({counter}){target.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1

def log_move(run_id: str,  source: Path, destination: Path) -> None:
    is_new = not LOG_FILE.exists()
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as log_file:
        log_writer = csv.writer(log_file, delimiter=',', lineterminator='\n')
        if is_new:
            log_writer.writerow(LOG_COLUMNS)
        log_writer.writerow([run_id, datetime.now().isoformat(timespec="seconds"), str(source), str(destination)])

def read_log() -> list[dict[str, str]]:
    """Read and print the contents of the log file."""
    if not Path(LOG_FILE).exists():
        print("Log file does not exist.")
        return []

    with open(LOG_FILE, 'r', newline='', encoding='utf-8') as log_file:
        log_reader = csv.DictReader(log_file)
        log_contents = list(log_reader)
        return log_contents

def write_log(rows: list[dict[str, str]]) -> None:
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=LOG_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

def undo_last_operations() -> None:
    """Undo the last file organization operation by moving files back to their original locations based on the log."""

    rows = read_log()
    if not rows:
        print("The log is empty. Nothing to undo.")
        return
 
    run_ids = sorted({row["run_id"] for row in rows})
 
    run_id = run_ids[-1]
    to_undo = [row for row in rows if row["run_id"] == run_id]
    
    if not to_undo:
        print(f"No run with ID {run_id} found in the log. Nothing to undo.")
        return
 
    failed: list[dict[str, str]] = []
    for row in reversed(to_undo):
        destination = Path(row["destination"])
        source = Path(row["source"])
 
        if not destination.exists():
            print(f"Skipping {destination.name}: no longer at {destination}")
            failed.append(row)
            continue
 
        target = unique_path(source)  # don't overwrite a file that appeared since
 
        try:
            shutil.move(destination, target)
            print(f"Restored {destination.name} to {target}")
        except OSError as err:
            print(f"Could not restore {destination.name}: {err}")
            failed.append(row)
 
    # Remove this run from the log, but keep any rows that failed so you can retry.
    remaining = [row for row in rows if row["run_id"] != run_id] + failed
    write_log(remaining)
    print(f"\nUndo of run {run_id} finished. {len(to_undo) - len(failed)} restored, "
          f"{len(failed)} kept in the log.") 
