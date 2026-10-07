import csv
from pathlib import Path
import shutil

from datetime import datetime
from utils import unique_path

LOG_FILE = Path(__file__).parent / "file_log.csv"
LOG_COLUMNS = ["run_id", "timestamp", "source", "destination"]

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
