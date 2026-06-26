from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PromptRun:
    query: dict[str, Any]
    geo: dict[str, str]
    repetition: int
    mode: str


class SampleResponseStore:
    def __init__(self, path: Path):
        self.path = path
        self._records = self._load()

    def _load(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        if not records:
            raise ValueError(f"No sample records found in {self.path}")
        return records

    def get(self, engine: str, query: dict[str, Any], repetition: int) -> dict[str, Any]:
        matching = [
            record
            for record in self._records
            if record["engine"] == engine and record["query_group"] == query["group"]
        ]
        pool = matching or [record for record in self._records if record["engine"] == engine] or self._records
        selected = pool[(repetition - 1) % len(pool)]
        copied = json.loads(json.dumps(selected))
        copied["query_id"] = query["id"]
        copied["query_group"] = query["group"]
        copied["query_text"] = query["text"]
        copied["repetition"] = repetition
        return copied


class EngineAdapter:
    engine_name = "base"
    model_name = "stub"

    def __init__(self, sample_store: SampleResponseStore | None = None):
        self.sample_store = sample_store

    def run(self, prompt_run: PromptRun) -> dict[str, Any]:
        if prompt_run.mode == "sample":
            if self.sample_store is None:
                raise ValueError("Sample mode requires a SampleResponseStore")
            return self.sample_store.get(self.engine_name, prompt_run.query, prompt_run.repetition)
        return self.live_stub(prompt_run)

    def live_stub(self, prompt_run: PromptRun) -> dict[str, Any]:
        return {
            "engine": self.engine_name,
            "model": self.model_name,
            "query_id": prompt_run.query["id"],
            "query_group": prompt_run.query["group"],
            "query_text": prompt_run.query["text"],
            "repetition": prompt_run.repetition,
            "answer_text": (
                "TODO: replace this placeholder with a real API response. "
                "Run sample mode until API keys and adapter calls are implemented."
            ),
            "citations": [],
            "adapter_status": "live_stub_not_implemented",
        }
