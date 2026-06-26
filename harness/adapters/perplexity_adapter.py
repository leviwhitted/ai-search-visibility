from __future__ import annotations

from .base import EngineAdapter, PromptRun


class PerplexitySonarAdapter(EngineAdapter):
    engine_name = "perplexity_sonar"
    model_name = "sonar_stub"

    def live_stub(self, prompt_run: PromptRun) -> dict:
        record = super().live_stub(prompt_run)
        record["todo"] = (
            "TODO: call Perplexity Sonar API, preserve returned citations, "
            "and keep the prompt/session stateless for each repetition."
        )
        record["required_env"] = ["PERPLEXITY_API_KEY"]
        return record
