# Folder Organizer

A simple Python project that organizes files in a selected folder by file type. It was created as a practice project after reading _Automate the Boring Stuff with Python_ by Al Sweigart.

## What it does

The script scans a target directory and moves files into category folders such as:

- Images
- Documents
- Audio
- Videos
- Archives
- Scripts
- Others

Files are grouped by their file extension, which makes it easier to keep download folders or project folders tidy.

## How to run

Run the batch file and pass the folder you want to organize.

```bat
folder_organizer.bat "C:\Users\User\Downloads"
```

You can also run the Python script directly:

```bash
python main.py
```

## Optional parameters

The main function supports these optional arguments:

```python
organize_folder(folder, add_date=True, move_old_files=False)
```

- `add_date=True`: rename the file as appending last modified date. Example: `2026-10-06_photo.jpg`.
- `move_old_files=False`: keeps older files in their normal category folder.
- `move_old_files=True`: moves files older than 30 days into `Old_Files/<Category>`, so they are separated from newer files.

This is useful when you want a cleaner archive and a backup-like structure for older items without deleting anything.

## Example

If a folder contains:

- `photo.jpg`
- `notes.txt`
- `video.mp4`
- `archive.zip`

The script moves them into matching folders such as `Images`, `Documents`, `Videos`, and `Archives`.

## Notes

- Category folders are created automatically when needed.
- Files that do not match a known extension are moved to `Others`.
- This is a small utility for quick file organization and cleanup.
