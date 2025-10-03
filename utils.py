
import fnmatch
import os
from pathlib import Path
from typing import Iterable

from .config import MAX_BYTES_PER_FILE, SKIP_DIRS, SKIP_FILE_GLOBS


def number_lines(text: str) -> str:
    lines = text.splitlines()
    return "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines))


def read_text_safe(path: Path, max_bytes: int = MAX_BYTES_PER_FILE) -> str:
    with path.open("rb") as f:
        data = f.read(max_bytes)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="ignore")


def should_skip_dir(dirpath: str) -> bool:
    base = os.path.basename(dirpath)
    return base in SKIP_DIRS


def should_skip_file(filename: str) -> bool:
    return any(fnmatch.fnmatch(filename, pat) for pat in SKIP_FILE_GLOBS)