from typing import Iterable, Literal, Optional, Union, Any, TypeVar
from openai._resource import SyncAPIResource, AsyncAPIResource
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion
from ffm.openai.lib.streaming import FfmAsyncStream
from ffm.openai.types.chat.chat_complection_chunk import FfmChatCompletionChunk
from ffm.openai.types.chat.chat_completion import FfmChatCompletion
from openai._streaming import Stream, AsyncStream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat_model import ChatModel
from openai.types.chat import completion_create_params
from openai._types import NotGiven, NOT_GIVEN, Body, Headers, Query, ResponseT
from openai._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from openai._base_client import make_request_options
import httpx

# from app.core.openai.lib.ffm import FfmOpenAI

_StreamT = TypeVar("_StreamT", bound=Stream[Any])

class Completions(SyncAPIResource):
    
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel],
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FfmChatCompletion | Stream[FfmChatCompletionChunk]:
        
        response =  self._post(
            path="/conversation",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "parameters" : {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "frequency_penalty": frequency_penalty
                    },
                    "stream": stream
                },
                completion_create_params.CompletionCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            files=None,
            cast_to=FfmChatCompletion,
            stream=stream or False,
            stream_cls=Stream[FfmChatCompletionChunk]
        )

        return response

class AsyncCompletions(AsyncAPIResource):

    async def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel],
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FfmChatCompletion | AsyncStream[FfmChatCompletionChunk]:
        response = await self._post(
            path="/conversation",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "parameters" : {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "frequency_penalty": frequency_penalty
                    },
                    "stream": stream
                },
                completion_create_params.CompletionCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),            
            cast_to=FfmChatCompletion,
            stream=stream or False,
            stream_cls=FfmAsyncStream[FfmChatCompletionChunk]
        )

        return response
    