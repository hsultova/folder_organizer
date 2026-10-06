# Folder organizer

A simple Python script that organizes files in a selected folder by file type into category subfolders. Used for practice after reading the book: _"Automate the boring stuff with pyrhon", AL SWEIGART_

## What it does

The script scans a target directory and moves files into folders such as:

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

## Example

If a folder contains:

- `photo.jpg`
- `notes.txt`
- `video.mp4`
- `archive.zip`

The script will place them into matching category folders such as `Images`, `Documents`, `Videos`, and `Archives`.

## Notes

- The script creates category folders automatically when needed.
- Files that do not match a known category are moved to the `Others` folder.
- This project is intended for quick file organization and cleanup.
