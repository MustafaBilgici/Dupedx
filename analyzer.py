
import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from .config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_OUTPUT_TOKENS


class Analyzer:

    def __init__(
        self,
        client: Optional[OpenAI] = None,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_output_tokens: int = MAX_OUTPUT_TOKENS,
    ) -> None:
        self.client = client or OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def analyze_code(
        self,
        code_with_numbers: str,
        file_path: str,
        system_prompt: str,
    ) -> List[Dict[str, Any]]:

        instruction = (
            "Scan this file and return JSON only. The output must be a JSON object, and the findings must be in an array named 'results'.\n"
            f"FILE_PATH: {file_path}\n"
            "```code\n" + code_with_numbers + "\n```"
        )

        try:
            resp = self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=instruction,
                text={"format": {"type": "json_object"}},
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )
        except Exception:
            return []

        raw = getattr(resp, "output_text", "")
        if not raw:
            return []

        findings: List[Dict[str, Any]] = []
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                if isinstance(data.get("results"), list):
                    findings = data["results"]
                elif isinstance(data.get("result"), dict):
                    findings = [data["result"]]
            elif isinstance(data, list):
                findings = data
        except Exception:
            findings = []

        for item in findings:
            item.setdefault("file_path", file_path)
        return findings