from typing import Any

from langchain_core.callbacks.base import BaseCallbackHandler

from notdiamond.llms.provider import NDLLMProvider


class NDLLMBaseCallbackHandler(BaseCallbackHandler):
    """
    Base callback handler for NotDiamond LLMs.
    Accepts all of the langchain_core callbacks and adds new ones.
    """

    def on_model_select(
        self, model_provider: NDLLMProvider, model_name: str
    ) -> Any:
        """
        Called when a model is selected.
        """

    def on_latency_tracking(
        self,
        session_id: str,
        model_provider: NDLLMProvider,
        tokens_per_second: float,
    ):
        """
        Called when latency tracking is enabled.
        """

    def on_api_error(self, error_message: str):
        """
        Called when an NDLLM API error occurs.
        """
