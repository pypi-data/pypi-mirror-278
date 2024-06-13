"""Ffm chat wrapper."""
from __future__ import annotations

import logging
import os
from typing import Any, AsyncIterator, Dict, Iterator, List, Mapping, Optional, Type, Union, cast
from langchain.schema import AIMessage, BaseMessage, ChatGeneration
from langchain_core.callbacks import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.messages import AIMessageChunk, BaseMessageChunk
from typing_extensions import override

import openai
from langchain_core.outputs import ChatGenerationChunk, ChatResult
from langchain_core.pydantic_v1 import Field, SecretStr, root_validator
from langchain_core.utils import convert_to_secret_str, get_from_dict_or_env

from langchain_openai.chat_models.base import BaseChatOpenAI

from ffm.openai.lib.ffm import AsyncFfmOpenAI, FfmOpenAI

logger = logging.getLogger(__name__)

def _convert_data_to_message_chunk(
    _dict: Mapping[str, Any], default_class: Type[BaseMessageChunk]
) -> BaseMessageChunk:
    content = cast(str, _dict.get("generated_text") or "")
    return default_class(content=content, id=None)     # type: ignore

class FfmChatOpenAI(BaseChatOpenAI):
    """提供LangChain整合的台智雲API用戶端
    
    對應BaseChatOpenAI的屬性設定如下
    client: 同步用戶端，序用
    async_client: 非同步用戶端，續用
    model_name: 沒用到，改用ffm_deployment
    temperature: 續用
    model_kwargs: 續用
    openai_api_key:
    openai_api_base:
    openai_organization: 沒用到
    openai_proxy: 沒用到
    request_timeout: 有用到
    max_retries: 有用到
    streaming: 有用到
    n: 沒用到
    max_token: 有用到
    tiktoken_model_name: 沒用到
    default_headers: 沒用到
    default_query: 沒用到
    http_client: 有用到
    http_async_client: 有用到
    """

    ffm_endpoint: Union[str, None] = None
    """台智雲API端點，必須是以api結尾，如果是公用端點，則是 https://api-ams.twcc.ai/api"""

    deployment_name: Union[str, None] = Field(default=None, alias="ffm_deployment")
    """佈署模型名稱，以llama3-70B為例是ffm-llama3-70b-chat"""
    
    ffm_api_key: Optional[SecretStr] = Field(default=None, alias="api_key")
    """台智雲API金鑰"""

    top_p: float = 1.0
    """預設的top p參數"""

    top_k: int = 100
    """預設的top k參數"""

    frequency_penalty: float = 1.0
    """頻率懲罰因數"""
    
    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object"""
        return ['app', 'core', 'langchain', 'language_model', 'ffm']
    

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {
            "openai_api_key": "OPENAI_API_KEY"
        }
    
    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""                
        
        openai_api_key = (
            values['ffm_api_key']
            or os.getenv("FFM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
        )
        values['openai_api_key'] = (
            convert_to_secret_str(openai_api_key) if openai_api_key else None
        )
        values["openai_api_base"] = values["openai_api_base"] or os.getenv(
            "OPENAI_API_BASE"
        )

        values["ffm_endpoint"] = values["ffm_endpoint"] or os.getenv(
            "FFM_ENDPOINT"
        )        

        client_params = {                        
            "api_key": values["openai_api_key"].get_secret_value()
            if values["openai_api_key"]
            else None,                                                
            "api_url": values["ffm_endpoint"],
            "timeout": values["request_timeout"],
            "max_retries": values["max_retries"],            
        }

        if not values.get("client"):
            sync_specific = {"http_client": values["http_client"]}
            values["client"] = FfmOpenAI(
                **client_params, **sync_specific
            ).chat.completions
        if not values.get("async_client"):            
            async_specific = {"http_client": values["http_async_client"]}
            values["async_client"] = AsyncFfmOpenAI(
                **client_params, **async_specific
            ).chat.completions
        return values
            
    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        params = {
            "model": self.deployment_name,
            "stream": self.streaming,            
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,            
            "frequency_penalty": self.frequency_penalty,
            **self.model_kwargs,
        }
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        return params
    
    def _create_chat_result(
            self, response: Union[dict, openai.BaseModel]
    ) -> ChatResult:
        
        logger.info(f"response: {response}")

        if not isinstance(response, dict):
            response = response.model_dump()
        
        if response.get("error"):
            raise ValueError(response.get("error"))

        chat_generation = ChatGeneration(            
            message = AIMessage(content=response.get('generated_text')),
            generation_info = {
                "token_usage": response.get("generated_tokens"), 
                "model": self.deployment_name,
                "finish_reason": response.get("finish_reason")
            }
        )        
        llm_output = {
            "token_usage": {
                "total_tokens": response.get("total_tokens"),
                "prompt_tokens": response.get("prompt_tokens"),
                "completion_tokens": response.get("generated_tokens")
            },
            "model_name": self.deployment_name
        }

        return ChatResult(generations=[chat_generation], llm_output=llm_output)
    @override
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        message_dicts, params = self._create_message_dicts(messages, stop)
        params = {**params, **kwargs, "stream": True}

        default_chunk_class = AIMessageChunk
        with self.client.create(messages=message_dicts, **params) as response:
            for chunk in response:
                if not isinstance(chunk, dict):
                    chunk = chunk.model_dump()                    
                          
                generation_info = {}
                if finish_reason := chunk["finish_reason"]:
                    generation_info["finish_reason"] = finish_reason                    

                chunk = _convert_data_to_message_chunk(
                    chunk, default_chunk_class
                )
                                
                default_chunk_class = chunk.__class__
                chunk = ChatGenerationChunk(
                    message=chunk, generation_info=generation_info or None
                )
                if run_manager:
                    run_manager.on_llm_new_token(
                        chunk.text, chunk=chunk, logprobs=None
                    )
                yield chunk
    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        message_dicts, params = self._create_message_dicts(messages, stop)
        params = {**params, **kwargs, "stream": True}

        default_chunk_class = AIMessageChunk
        response = await self.async_client.create(messages=message_dicts, **params)
        async with response:
            async for chunk in response:
                if not isinstance(chunk, dict):
                    chunk = chunk.model_dump()                    
                
                generation_info = {}
                if finish_reason := chunk["finish_reason"]:
                    generation_info["finish_reason"] = finish_reason

                chunk = _convert_data_to_message_chunk(
                    chunk, default_chunk_class
                )
                
                default_chunk_class = chunk.__class__
                chunk = ChatGenerationChunk(
                    message=chunk, generation_info=generation_info or None
                )
                if run_manager:
                    await run_manager.on_llm_new_token(
                        chunk.text, chunk=chunk, logprobs=None
                    )
                yield chunk

    