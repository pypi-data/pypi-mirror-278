from typing import Iterable, Literal, Optional, Union
from openai._resource import SyncAPIResource, AsyncAPIResource
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from ffm.openai.lib.streaming import FfmAsyncStream
from ffm.openai.types.chat.chat_complection_chunk import FfmChatCompletionChunk
from ffm.openai.types.chat.chat_completion import FfmChatCompletion
from openai._streaming import Stream, AsyncStream
from openai.types.chat_model import ChatModel
from openai.types.chat import completion_create_params
from openai._types import NotGiven, NOT_GIVEN, Body, Headers, Query
from openai._utils import (    
    maybe_transform,
    async_maybe_transform,
)
from openai._base_client import make_request_options
import httpx

class Completions(SyncAPIResource):
    """Chat Completion的同步版本"""
    
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
        """進行chat completions 同步API呼叫

        Args:
            messages (Iterable[ChatCompletionMessageParam]): 訊息內容
            model (Union[str, ChatModel]): 模型
            max_tokens (Optional[int] | NotGiven, optional): 最大輸出token. Defaults to NOT_GIVEN.
            temperature (Optional[float] | NotGiven, optional): 溫度參數. Defaults to NOT_GIVEN.
            top_k (Optional[int] | NotGiven, optional): Top K參數，top-k參數是用於控制模型在生成文本時的選擇範圍 Defaults to NOT_GIVEN.
            top_p (Optional[float] | NotGiven, optional): Top P參數，從這k個詞中，再根據累積概率達到p的詞集合中進行篩選. Defaults to NOT_GIVEN.
            frequency_penalty (Optional[float] | NotGiven, optional): 頻率懲罰（frequency penalty）是一種用於調整大型語言模型生成文本的技術，旨在避免模型過度重複使用某些詞或詞組。. Defaults to NOT_GIVEN.
            stream (Optional[Literal[False]] | Literal[True] | NotGiven, optional): 是否要啟用流式輸出. Defaults to NOT_GIVEN.
            extra_headers (Headers | None, optional): 額外的http header. Defaults to None.
            extra_query (Query | None, optional): 額外的query. Defaults to None.
            extra_body (Body | None, optional): 額外的查詢本體. Defaults to None.
            timeout (float | httpx.Timeout | None | NotGiven, optional): 逾時設定. Defaults to NOT_GIVEN.

        Returns:
            FfmChatCompletion | Stream[FfmChatCompletionChunk]: 交談結果或流式輸出的結果
        """
        
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
    """進行chat completions 非同步API呼叫

        Args:
            messages (Iterable[ChatCompletionMessageParam]): 訊息內容
            model (Union[str, ChatModel]): 模型
            max_tokens (Optional[int] | NotGiven, optional): 最大輸出token. Defaults to NOT_GIVEN.
            temperature (Optional[float] | NotGiven, optional): 溫度參數. Defaults to NOT_GIVEN.
            top_k (Optional[int] | NotGiven, optional): Top K參數，top-k參數是用於控制模型在生成文本時的選擇範圍 Defaults to NOT_GIVEN.
            top_p (Optional[float] | NotGiven, optional): Top P參數，從這k個詞中，再根據累積概率達到p的詞集合中進行篩選. Defaults to NOT_GIVEN.
            frequency_penalty (Optional[float] | NotGiven, optional): 頻率懲罰（frequency penalty）是一種用於調整大型語言模型生成文本的技術，旨在避免模型過度重複使用某些詞或詞組。. Defaults to NOT_GIVEN.
            stream (Optional[Literal[False]] | Literal[True] | NotGiven, optional): 是否要啟用流式輸出. Defaults to NOT_GIVEN.
            extra_headers (Headers | None, optional): 額外的http header. Defaults to None.
            extra_query (Query | None, optional): 額外的query. Defaults to None.
            extra_body (Body | None, optional): 額外的查詢本體. Defaults to None.
            timeout (float | httpx.Timeout | None | NotGiven, optional): 逾時設定. Defaults to NOT_GIVEN.

        Returns:
            FfmChatCompletion | Stream[FfmChatCompletionChunk]: 交談結果或流式輸出的結果
    """

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
    
    