from pathlib import Path

def next_available_path(target: Path) -> Path:
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