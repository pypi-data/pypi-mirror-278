"""
Format utilities
"""


def human_readable_size(size: int) -> str:
    """Convert a file size in bytes to a human-readable format."""
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"  # If it's bigger than TB, return in petabytes.
