import argparse
import json

try:

    from .config import DEFAULT_MODEL
    from .prompts import SYSTEM_PROMPT_BASE, CLOUD_PROMPT_ADDON, ACCESS_CONTROL_PROMPT_ADDON
    from .analyzer import Analyzer
    from .scanner import Scanner, build_exts
except ImportError:  
    import sys
    from pathlib import Path


    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from sast_scanner.config import DEFAULT_MODEL
    from sast_scanner.prompts import (
        SYSTEM_PROMPT_BASE, CLOUD_PROMPT_ADDON, ACCESS_CONTROL_PROMPT_ADDON
    )
    from sast_scanner.analyzer import Analyzer
    from sast_scanner.scanner import Scanner, build_exts

def run() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Directory-based, LLM-powered SAST scanner "
            "(SQLi, XSS, Insecure Deserialization, SSRF, RCE, SSTI). "
            "Optional --cloudscan adds IaC checks; --acscan adds access-control checks."
        )
    )
    parser.add_argument("directory", help="Root directory to scan")
    parser.add_argument("--out", default="report.json", help="Path for JSON report (default: report.json)")
    parser.add_argument("--cloudscan", action="store_true", help="Enable cloud checks and include IaC/policy files")
    parser.add_argument("--acscan", action="store_true", help="Include access-control (AUTHZ_*) vulnerability checks")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name (e.g., gpt-4.1, gpt-4o, etc.)")

    args = parser.parse_args()

    system_prompt = SYSTEM_PROMPT_BASE
    if args.cloudscan:
        system_prompt += CLOUD_PROMPT_ADDON
    if args.acscan:
        system_prompt += ACCESS_CONTROL_PROMPT_ADDON

    exts = build_exts(args.cloudscan)

    analyzer = Analyzer(model=args.model)
    scanner = Scanner(exts=exts, analyzer=analyzer, system_prompt=system_prompt)

    report = scanner.scan_directory(args.directory)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(
        f"✓ Scan finished. {len(report['scanned_files'])} file checked, "
        f"{len(report['findings'])} finding created."
    )
    print(f"Rapor: {args.out}")


if __name__ == "__main__":
    run()