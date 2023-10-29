import os


def ensure_dir(path: str) -> None:
    """
    Ensure the existence of a directory
    and all its parent folders. Creates
    all parents on route.
    """
    
    try:
        os.makedirs(path)
    except OSError:
        pass
