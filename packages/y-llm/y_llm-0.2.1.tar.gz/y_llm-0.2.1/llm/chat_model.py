from typing import Any, Dict, Iterator, List, Optional
from urllib.parse import urljoin

import httpx
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from openai.types.chat import ChatCompletion


class ProxyChatModel(BaseChatModel):
    api_key: str
    endpoint: str
    provider: str = "azure"
    model: str = "proxy"
    timeout: int = 60 * 5

    # chat related
    # Definitions taken from https://platform.openai.com/docs/api-reference/chat/create?lang=python
    frequency_penalty: int = 0
    logit_bias: Any = None
    logprobs: bool | None = None
    top_logprobs: int | None = None
    max_tokens: int | None = None
    n: int = 1
    presence_penalty: int = 0
    response_format: str | None = None
    seed: int | None = None
    stop: str | list | None = None
    # stream: bool = False
    temperature: float = 0.0
    top_p: float = 1
    user: str | None = None

    @property
    def _llm_type(self) -> str:
        return f"proxy-server:{self.model}"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.model,
        }

    @staticmethod
    def _format_message(message: BaseMessage) -> dict:
        if isinstance(message, SystemMessage):
            return {
                "content": message.content,
                "role": "system",
            }
        if isinstance(message, HumanMessage):
            return {
                "content": message.content,
                "role": "user",
            }
        if isinstance(message, AIMessage):
            return {
                "content": message.content,
                "role": "assistant",
            }
        raise ValueError(f"Unknown message type: {type(message)}")

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        with httpx.Client() as client:
            formatted_messages = [self._format_message(message) for message in messages]
            config = "{}"
            res = client.post(
                urljoin(
                    self.endpoint,
                    f"/openai/deployments/{self.model}/chat/completions?api-version={config}",
                ),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={
                    **{
                        # proxy related
                        "provider": self.provider,
                        "meta": run_manager.metadata,
                        # chat related
                        "model": self.model,
                        "messages": formatted_messages,
                        "frequency_penalty": self.frequency_penalty,
                        "logit_bias": self.logit_bias,
                        "logprobs": self.logprobs,
                        "top_logprobs": self.top_logprobs,
                        "max_tokens": self.max_tokens,
                        "n": self.n,
                        "presence_penalty": self.presence_penalty,
                        "response_format": self.response_format,
                        "seed": self.seed,
                        "stop": self.stop,
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                        "user": self.user,
                    },
                    **kwargs,
                },
                timeout=self.timeout,
            )
            if res.status_code != 200:
                raise Exception(f"Failed to generate chat: {res.json()}")

            # build response
            body = ChatCompletion(**res.json())
            generations = [
                ChatGeneration(
                    message=AIMessage(
                        content=choice.message.content,
                    )
                )
                for choice in body.choices
            ]
            return ChatResult(generations=generations, llm_output=None)

        raise Exception("Failed to generate chat")

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        raise NotImplementedError("Streaming is not supported for this model.")
