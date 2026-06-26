from __future__ import annotations

from .base import EngineAdapter, PromptRun


class GeminiGroundingAdapter(EngineAdapter):
    engine_name = "gemini_grounding"
    model_name = "gemini_search_grounding_stub"

    def live_stub(self, prompt_run: PromptRun) -> dict:
        record = super().live_stub(prompt_run)
        record["todo"] = (
            "TODO: call Gemini API with Google Search grounding, "
            "capture grounding chunks/URLs, and label output as API-grounded sample."
        )
        record["required_env"] = ["GEMINI_API_KEY"]
        return record
