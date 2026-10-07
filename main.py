import argparse

from folder_organizer import OLD_FILE_AGE_DAYS, organize_folder

def parse_args() -> argparse.Namespace:
    """Build the command-line interface and parse the given arguments."""
    parser = argparse.ArgumentParser(description="Organize the files in a folder by file type.")
    parser.add_argument("folder", help="path to the folder you want to organize")
    parser.add_argument(
        "--no-date",
        dest="add_date",
        action="store_false",
        help="keep the original filenames instead of prepending the last modified date",
    )
    parser.add_argument(
        "--move-old-files",
        action="store_true",
        help=f"move files older than {OLD_FILE_AGE_DAYS} days into Old_Files/<Category>",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="undo the most recent organization run instead of organizing",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    organize_folder(
        args.folder,
        add_date=args.add_date,
        move_old_files=args.move_old_files,
        undo=args.undo,
    )

if __name__ == "__main__":
    main()
