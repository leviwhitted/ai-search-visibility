from __future__ import annotations

from .base import EngineAdapter, PromptRun


class OpenAIWebSearchAdapter(EngineAdapter):
    engine_name = "openai_web_search"
    model_name = "responses_api_web_search_stub"

    def live_stub(self, prompt_run: PromptRun) -> dict:
        record = super().live_stub(prompt_run)
        record["todo"] = (
            "TODO: call OpenAI Responses API with web search enabled, "
            "temperature near 0, fixed geo where supported, and citation capture."
        )
        record["required_env"] = ["OPENAI_API_KEY"]
        return record
