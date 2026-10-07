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

def organize_folder(folder: str, add_date: bool = True, move_old_files: bool = False) -> None:
    """
    Organize files in the specified folder based on their extensions. 
    Optionally, add the date to the filename and move old files to a separate folder.
    :param folder: The path to the folder to organize.
    :param add_date: Whether to add the date to the filename (default is True).
    :param move_old_files: Whether to move old files to a separate folder (default is False).
    """
    folder_path = Path(folder)
    if not folder_path.exists():    
        print(f"The folder '{folder}' does not exist.")
        return

    for file in folder_path.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            is_moved = False

            for category, extensions in FILE_TYPES.items():
                if file_extension in extensions:
                    category_path = folder_path / category
                    if move_old_files and is_file_old(file):
                        category_path = folder_path / 'Old_Files' / category
                        
                    try:
                        move_file(file, category_path, add_date)
                        is_moved = True
                    except OSError as err:
                        print(f"Could not move {file.name}: {err}")
                        continue
                    break

            if not is_moved:
                others_path = folder_path / 'Others'
                if move_old_files and is_file_old(file):
                    others_path = folder_path / 'Old_Files' / 'Others'
                try:
                    move_file(file, others_path, add_date)
                except OSError as err:
                    print(f"Could not move {file.name}: {err}")
                    continue

def move_file(file: Path, folder_to_move: Path, add_date: bool) -> None:
    """Move a file to the specified folder. If the folder does not exist, create it.
    Optionally, add the date to the filename.
    """
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")    

    folder_to_move.mkdir(parents=True, exist_ok=True)
    file_name = file.name    
    file_to_move = folder_to_move / file_name
    if add_date:
        regex = r'\d{2,4}[-._]\d{2}[-._]\d{2,4}'
        if re.search(regex, file_name):
            print(f"File '{file_name}' already has a date in its name. Skipping date addition.")
        else:
            date = datetime.fromtimestamp(file.stat().st_mtime).date()
            file_name = f"{date}_{file.name}"
            file_to_move = folder_to_move / file_name
            print(f"Renamed '{file_name}' to '{f'{date}_{file.name}'}'")


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
