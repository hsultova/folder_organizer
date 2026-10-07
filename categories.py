# Define the categories and their associated file extensions
CATEGORY_EXTENSIONS = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.ipynb'],
}

def category_for(extension: str) -> str:
    """Return the category folder name for a file extension."""
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category
    return "Others"