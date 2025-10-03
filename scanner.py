
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

from .config import BASE_CODE_EXTS, CLOUD_EXTS
from .utils import number_lines, read_text_safe, should_skip_dir, should_skip_file
from .analyzer import Analyzer


class Scanner:
    def __init__(self, exts: Set[str], analyzer: Analyzer, system_prompt: str) -> None:
        self.exts = set(exts)
        self.analyzer = analyzer
        self.system_prompt = system_prompt

    def scan_directory(self, root: str) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []
        scanned_files: List[str] = []

        for dirpath, dirnames, filenames in os.walk(root):

            dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]

            for fn in filenames:
                if should_skip_file(fn):
                    continue
                p = Path(dirpath) / fn
                if p.suffix.lower() not in self.exts:
                    continue
                scanned_files.append(str(p))

                text = read_text_safe(p)
                if not text.strip():
                    continue

                numbered = number_lines(text)
                results = self.analyzer.analyze_code(numbered, str(p), self.system_prompt)
                if results:
                    findings.extend(results)

        return {
            "scanned_root": os.path.abspath(root),
            "scanned_files": scanned_files,
            "findings": findings,
        }


def build_exts(use_cloudscan: bool) -> Set[str]:
    exts = set(BASE_CODE_EXTS)
    if use_cloudscan:
        exts |= CLOUD_EXTS
    return exts