
from pathlib import Path
from typing import Set


BASE_CODE_EXTS: Set[str] = {
    ".py", ".js", ".ts", ".tsx", ".java", ".php", ".go", ".cs", ".rb",
    ".html", ".htm", ".jsp", ".jinja", ".twig", ".vue",
    ".yaml", ".yml",
}

CLOUD_EXTS: Set[str] = {

    ".tf", ".tfvars", ".tf.json", ".hcl",

    ".template", ".cfn.yaml", ".cfn.yml",

    ".policy.json",
}

MAX_BYTES_PER_FILE: int = 512_000  

DEFAULT_MODEL = "gpt-4.1" 
DEFAULT_TEMPERATURE = 0
MAX_OUTPUT_TOKENS = 2000


SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", ".idea", ".vscode", "dist", "build", "__pycache__",
}


SKIP_FILE_GLOBS = {"*.min.js", "*.lock", "package-lock.json"}
