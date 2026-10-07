# Folder Organizer

A simple Python project that organizes files in a selected folder by file type. It was created as a practice project after reading _Automate the Boring Stuff with Python_ by Al Sweigart.

## What it does

The script scans a target directory and moves each file into a category folder based on its extension:

| Category    | Extensions                            |
| ----------- | ------------------------------------- |
| `Images`    | `.jpg` `.jpeg` `.png` `.gif` `.bmp`   |
| `Documents` | `.pdf` `.docx` `.txt` `.xlsx` `.pptx` |
| `Audio`     | `.mp3` `.wav` `.aac`                  |
| `Videos`    | `.mp4` `.avi` `.mov` `.mkv`           |
| `Archives`  | `.zip` `.rar` `.tar` `.gz`            |
| `Scripts`   | `.py` `.js` `.html` `.css` `.ipynb`   |
| `Others`    | anything that doesn't match the above |

## How to run

Run the batch file and pass the folder you want to organize.

```bat
folder_organizer.bat "C:\Users\User\Downloads"
```

Or run the Python script directly:

```bash
python main.py "C:\Users\User\Downloads"
```

The folder is required. Run `python main.py --help` to see the available options.

## Options

```
usage: main.py [-h] [--no-date] [--move-old-files] [--undo] folder
```

- `--no-date`: keep the original filenames. By default the file's modification date is prepended, giving names like `2026-10-06_photo.jpg`; names that already contain something date-like are left alone either way.
- `--move-old-files`: files older than 30 days go into `Old_Files/<Category>` instead of `<Category>`, so an archive stays separate from recent downloads.
- `--undo`: skip organizing and reverse the most recent run instead. See below.

For example, to archive old files without renaming anything:

```bash
python main.py "C:\Users\User\Downloads" --no-date --move-old-files
```

The same options are available if you'd rather import the function:

```python
from folder_organizer import organize_folder

organize_folder(r"C:\Users\User\Downloads", add_date=False, move_old_files=True)
```

If a file with the target name already exists, a counter is added rather than overwriting it — for example `report (1).pdf`.

## Logging and undo

Every successful move is appended to `file_log.csv`, which lives next to the scripts (not in the organized folder). A row is written only after the move succeeds, so the log never lists a move that didn't happen.

### Log format

| Column        | Description                                |
| ------------- | ------------------------------------------ |
| `run_id`      | Shared by every file moved in the same run |
| `timestamp`   | When the file was moved                    |
| `source`      | Where the file was before                  |
| `destination` | Where the file is now                      |

### Undoing

```python
organize_folder(folder, undo=True)
```

This reads the newest `run_id` from the log and moves those files back to their original paths, in reverse order, restoring their original names.

- Files that are no longer where the log says they are get skipped.
- If something new now occupies the original path, the restored file gets a counter instead of overwriting it.
- Rows for the undone run are removed from the log so the same run can't be undone twice. Rows that failed stay in the log so you can retry.

Because the log is shared across folders, an undo always applies to whichever run was most recent overall — not to a specific folder.

## Example

A folder containing `photo.jpg`, `notes.txt`, `video.mp4` and `archive.zip` becomes:

```
Images/2026-10-06_photo.jpg
Documents/2026-10-06_notes.txt
Videos/2026-10-06_video.mp4
Archives/2026-10-06_archive.zip
```

With `add_date=False` the filenames stay unchanged.

## Notes

- Category folders are created automatically when needed.
- Files that do not match a known extension are moved to `Others`.
- This is a small utility for quick file organization and cleanup.
