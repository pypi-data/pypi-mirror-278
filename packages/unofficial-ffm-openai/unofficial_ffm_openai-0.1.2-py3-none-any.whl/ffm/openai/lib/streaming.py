from typing import AsyncIterator, cast, Any
from typing_extensions import override
from openai import APIError, AsyncStream
from openai._streaming import _T
from openai._utils import is_mapping
import json
import logging

logger = logging.getLogger(__name__)


class FfmAsyncStream(AsyncStream[_T]):
    """繼承OpenAI內建非同步串流，覆寫__stream__方法以捕捉台智雲模型在長文本輸出狀況下的流式輸出異常

    Args:
        AsyncStream (_type_): OpenAI內建的非同步串流類別

    Raises:
        APIError: 意外狀況下會拋出APIError例外

    Yields:
        _type_: 處理過得片段內容
    """

    @override
    async def __stream__(self) -> AsyncIterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        async for sse in iterator:
            if sse.data.startswith("[DONE]"):
                break

            if sse.event is None:                
                try:
                    data = sse.json() # 這裡，台智雲模型可能會不符合JSON解析規則
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")                    
                    continue

                if is_mapping(data) and data.get("error"):
                    message = None
                    error = data.get("error")
                    if is_mapping(error):
                        message = error.get("message")
                    if not message or not isinstance(message, str):
                        message = "An error occurred during streaming"

                    raise APIError(
                        message=message,
                        request=self.response.request,
                        body=data["error"],
                    )

                yield process_data(data=data, cast_to=cast_to, response=response)

            else:
                try:
                    data = sse.json()
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")                    
                    continue

                if sse.event == "error" and is_mapping(data) and data.get("error"):
                    message = None
                    error = data.get("error")
                    if is_mapping(error):
                        message = error.get("message")
                    if not message or not isinstance(message, str):
                        message = "An error occurred during streaming"

                    raise APIError(
                        message=message,
                        request=self.response.request,
                        body=data["error"],
                    )

                yield process_data(data={"data": data, "event": sse.event}, cast_to=cast_to, response=response)

        # Ensure the entire stream is consumed
        async for _sse in iterator:
            ...