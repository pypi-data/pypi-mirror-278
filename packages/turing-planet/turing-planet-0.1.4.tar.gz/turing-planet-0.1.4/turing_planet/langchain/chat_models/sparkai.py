# copy from https://github.com/vsxd/langchain/blob/feature-add-spark-llm/libs/langchain/langchain/chat_models/sparkllm.py

import logging
from typing import Any, Dict, Iterator, List, Mapping, Optional, Type

from turing_planet.api.spark_chat_client import SparkLLMClient

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models.base import (
    BaseChatModel,
    generate_from_stream,
)
from langchain.pydantic_v1 import Field, root_validator
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatGeneration,
    ChatMessage,
    ChatResult,
    HumanMessage,
    SystemMessage,
)
from langchain.schema.messages import (
    AIMessageChunk,
    BaseMessageChunk,
    ChatMessageChunk,
    HumanMessageChunk, FunctionMessage,
)
from langchain.schema.output import ChatGenerationChunk
from langchain.utils import (
    get_from_dict_or_env,
    get_pydantic_field_names,
)

logger = logging.getLogger(__name__)


def _convert_message_to_dict(message: BaseMessage) -> dict:
    if isinstance(message, ChatMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    elif isinstance(message, FunctionMessage):
        message_dict = {"role": "assistant", "content": message.content}
    else:
        raise ValueError(f"Got unknown type {message}")

    return message_dict


def _convert_dict_to_message(_dict: Mapping[str, Any]) -> AIMessage:
    content = _dict.get("content", "") or ""
    if _dict.get("function_call"):
        additional_kwargs = {"function_call": dict(_dict["function_call"])}
        if "thoughts" in additional_kwargs["function_call"]:
            # align to api sample, which affects the llm function_call output
            additional_kwargs["function_call"].pop("thoughts")
    else:
        additional_kwargs = {}
    return AIMessage(
        content=content,
        additional_kwargs=additional_kwargs,
    )


def _convert_delta_to_message_chunk(
        _dict: Mapping[str, Any], default_class: Type[BaseMessageChunk]
) -> BaseMessageChunk:
    msg_role = _dict["role"]
    msg_content = _dict.get("content", "")
    if msg_role == "user" or default_class == HumanMessageChunk:
        return HumanMessageChunk(content=msg_content)
    elif msg_role == "assistant" or default_class == AIMessageChunk:
        return AIMessageChunk(content=msg_content)
    elif msg_role or default_class == ChatMessageChunk:
        return ChatMessageChunk(content=msg_content, role=msg_role)
    else:
        return default_class(content=msg_content)


class ChatSparkAI(BaseChatModel):
    """Wrapper around iFlyTek's Spark large language model.

    To use, you should pass `endpoint`as a named parameter to the constructor
    OR set environment variables ``TURING_PLANET_ENDPOINT``
    Example:
        .. code-block:: python

        client = ChatSparkAI(
            endpoint="<endpoint>",
        )
    """

    client: Any = None  #: :meta private:
    endpoint: Optional[str] = None

    trace_id: str = "langchain_user"
    max_tokens: int = 4096
    temperature: float = 0.5
    top_k: int = 4
    adjust_tokens: bool = True
    domain: str = ""

    streaming: bool = False
    request_timeout: int = 120

    model_kwargs: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this model can be serialized by Langchain."""
        return True

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = get_pydantic_field_names(cls)
        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name in extra:
                raise ValueError(f"Found {field_name} supplied twice.")
            if field_name not in all_required_field_names:
                logger.warning(
                    f"""WARNING! {field_name} is not default parameter.
                    {field_name} was transferred to model_kwargs.
                    Please confirm that {field_name} is what you intended."""
                )
                extra[field_name] = values.pop(field_name)

        invalid_model_kwargs = all_required_field_names.intersection(extra.keys())
        if invalid_model_kwargs:
            raise ValueError(
                f"Parameters {invalid_model_kwargs} should be specified explicitly. "
                f"Instead they were passed in as part of `model_kwargs` parameter."
            )

        values["model_kwargs"] = extra

        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values["endpoint"] = get_from_dict_or_env(
            values,
            "endpoint",
            "TURING_PLANET_ENDPOINT",
            "127.0.0.1:9980",
        )
        # put extra params into model_kwargs
        values["model_kwargs"]["max_tokens"] = values["max_tokens"]
        values["model_kwargs"]["temperature"] = values["temperature"]
        values["model_kwargs"]["top_k"] = values["top_k"]
        values["model_kwargs"]["adjust_tokens"] = values["adjust_tokens"]
        values["model_kwargs"]["domain"] = values["domain"]

        values["client"] = SparkLLMClient(
            endpoint=values["endpoint"],
            trace_id=values["trace_id"],
            model_kwargs=values["model_kwargs"],
        )
        return values

    def _stream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        default_chunk_class = AIMessageChunk

        self.client.arun(
            [_convert_message_to_dict(m) for m in messages],
            self.model_kwargs,
            kwargs,
            self.streaming,
        )
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "data" not in content:
                continue
            delta = content["data"]
            chunk = _convert_delta_to_message_chunk(delta, default_chunk_class)
            yield ChatGenerationChunk(message=chunk)
            if run_manager:
                run_manager.on_llm_new_token(str(chunk.content))

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = self._stream(
                messages=messages, stop=stop, run_manager=run_manager, **kwargs
            )
            return generate_from_stream(stream_iter)

        self.client.arun(
            [_convert_message_to_dict(m) for m in messages],
            self.model_kwargs,
            kwargs,
            False,
        )
        completion = {}
        llm_output = {}
        for content in self.client.subscribe(timeout=self.request_timeout):
            if "usage" in content:
                llm_output["token_usage"] = content["usage"]
            if "data" not in content:
                continue
            completion = content["data"]
        message = _convert_dict_to_message(completion)
        generations = [ChatGeneration(message=message)]
        return ChatResult(generations=generations, llm_output=llm_output)

    @property
    def _llm_type(self) -> str:
        return "spark-llm-chat"
