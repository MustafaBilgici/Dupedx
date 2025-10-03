# Dupedx LLM-Powered SAST / Cloud / Access Control Scanner


## What is this?

A CLI that sends **line-numbered** source files to the OpenAI Responses API and emits a JSON report of findings.

* Core rules: `SQLi`, `XSS`, `INSECURE DESERILIZATION`, `SSRF`, `RCE`, `SSTI`
* Optional: `CLOUD VULNERABILITIES` (IaC/Cloud), `AUTHERIZATION & BUSINESS LOGIC VULNERABILITIES*` (authorization)

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
```

## Quick Start

```bash
# package mode
python -m sast_scanner <DIR> --out report.json

# or direct
python path/to/main.py <DIR> --out report.json
```

Common examples:

```bash
python -m sast_scanner ./src                 # SAST only
python -m sast_scanner ./infra --cloudscan   # add Cloud/IaC
python -m sast_scanner ./app --acscan        # add Access Control
python -m sast_scanner . --cloudscan --acscan --model gpt-4.1
```

## CLI Flags

* `directory` (required) – root folder to scan
* `--out <file>` – JSON report path (default: `report.json`)
* `--cloudscan` – enable `CLOUD_*` checks
* `--acscan` – enable `AUTHZ_*` checks
* `--model <name>` – OpenAI model (default `gpt-4.1`)

## Output (JSON)

```json
{
  "scanned_root": "/abs/path",
  "scanned_files": ["/abs/file1.py"],
  "findings": [ { /* finding objects */ } ]
}
```

Each finding contains: `rule_id`, `title`, `severity`, `description`, `why`, `file_path`, `start_line`, `end_line`, `prevention`, `vuln_lines`.

## File Types

Default: `.py .js .ts .tsx .java .php .go .cs .rb .html .htm .jsp .jinja .twig .vue .yaml .yml`

With `--cloudscan`: `.tf .tfvars .tf.json .hcl .template .cfn.yaml .cfn.yml .policy.json`

## Limits & Skips

* Max file size ~500 KB
* Skip dirs: `.git`, `node_modules`, `.venv`, `venv`, `.idea`, `.vscode`, `dist`, `build`, `__pycache__`
* Ignore: `*.min.js`, `*.lock`, `package-lock.json`

## Config Defaults

`DEFAULT_MODEL=gpt-4.1`, `DEFAULT_TEMPERATURE=0`, `MAX_OUTPUT_TOKENS=2000`.
