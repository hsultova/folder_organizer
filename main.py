import sys
from folder_organizer import organize_folder

def main(folder_name: str) -> None:
    # folder_name is the path to the folder you want to organize
    organize_folder(folder_name)

if __name__ == "__main__":
    # Check if a folder name is provided as a command-line argument
    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
    else:
        # Specify the folder name directly if running the script without command-line arguments
        folder_name = r'D:\Projects\folder_organizer\downloads'
    main(folder_name)
