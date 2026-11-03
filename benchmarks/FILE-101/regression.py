from pathlib import Path
def resolve_file(root, name):
    if "/" in name or ".." in name or Path(name).is_absolute():
        raise ValueError("invalid")
    return Path(root).resolve() / name
