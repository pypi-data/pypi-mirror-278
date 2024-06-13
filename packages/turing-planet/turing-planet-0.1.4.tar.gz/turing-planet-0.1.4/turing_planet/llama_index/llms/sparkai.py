# 自定义大模型
from typing import Any, Optional, Sequence

from llama_index.core.base.llms.types import LLMMetadata, CompletionResponse, CompletionResponseGen, ChatMessage, ChatResponse, ChatResponseGen, MessageRole
from llama_index.core.llms import CustomLLM
from llama_index.core.llms.callbacks import llm_completion_callback, llm_chat_callback

from turing_planet.api.spark_chat_client import SparkLLMClient
from turing_planet.utils.env import get_from_dict_or_env


def _convert_prompt_to_dict(
        prompt: str,
) -> dict:
    return {"role": "user", "content": prompt}


class SparkAI(CustomLLM):
    client: Any = None

    context_window: int = 3900
    num_output: int = 256
    model_name: str = "sparkai"

    request_timeout: Optional[int] = 120

    def __init__(self,
                 trace_id: Optional[str] = "llamaIndex_user",
                 max_tokens: Optional[int] = 4096,
                 temperature: Optional[float] = 0.5,
                 top_k: Optional[int] = 4,
                 domain: Optional[str] = None,
                 **kwargs: Any):

        super().__init__(**kwargs)

        if "timeout" in kwargs:
            self.request_timeout = kwargs["timeout"]

        endpoint = get_from_dict_or_env(
            kwargs,
            "endpoint",
            "TURING_PLANET_ENDPOINT",
            "127.0.0.1:9980",
        )

        param = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "domain": domain,
        }

        self.client = SparkLLMClient(
            endpoint=endpoint,
            trace_id=trace_id,
            model_kwargs={**param, **kwargs},
        )

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        prompt = prompt.replace("\n", "\\n")

        self.client.arun(
            [_convert_prompt_to_dict(prompt)],
            None,
            kwargs,
            False,
        )

        completion = {}
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "data" not in content:
                continue
            completion = content["data"]

        return CompletionResponse(text=completion["content"])

    @llm_completion_callback()
    def stream_complete(
            self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        prompt = prompt.replace("\n", r"\\n")

        self.client.arun(
            [_convert_prompt_to_dict(prompt)],
            kwargs=kwargs,
            streaming=True,
        )

        response = ""
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "data" not in content:
                continue
            delta = content["data"]["content"]
            response += delta
            yield CompletionResponse(text=response, delta=delta)

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        chat_messages = []
        for message in messages:
            chat_messages.append({"role": message.role, "content": message.content})

        self.client.arun(
            chat_messages,
            None,
            kwargs,
            False,
        )

        completion = {}
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "data" not in content:
                continue
            completion = content["data"]
        return ChatResponse(message=ChatMessage.from_str(content=completion, role=MessageRole.ASSISTANT))

    @llm_chat_callback()
    def stream_chat(
            self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        chat_messages = []
        for message in messages:
            chat_messages.append({"role": message.role, "content": message.content})

        self.client.arun(
            chat_messages,
            kwargs=kwargs,
            streaming=True,
        )

        # response = ""
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "data" not in content:
                continue
            delta = content["data"]["content"]
            # response += delta
            yield ChatResponse(message=ChatMessage.from_str(content=delta, role=MessageRole.ASSISTANT), delta=delta)
