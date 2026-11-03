from pathlib import Path
def resolve_file(root, name):
    base = Path(root).resolve()
    if Path(name).is_absolute():
        raise ValueError("absolute path")
    target = (base / name).resolve()
    if target == base or not target.is_relative_to(base):
        raise ValueError("outside root")
    return target
