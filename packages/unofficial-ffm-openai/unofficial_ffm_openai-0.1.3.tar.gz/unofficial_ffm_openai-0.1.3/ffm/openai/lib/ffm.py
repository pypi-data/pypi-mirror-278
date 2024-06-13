import asyncio
from pyexpat import model
from typing import Any, TypeVar, Union, overload
from venv import create
import httpx
from openai import AsyncOpenAI, AsyncStream, OpenAI
from openai._base_client import BaseClient
from openai._models import FinalRequestOptions
from typing_extensions import Self, override
from openai._utils import is_mapping
from openai._types import NOT_GIVEN, Timeout, NotGiven
from openai._base_client import BaseClient
from openai._constants import DEFAULT_MAX_RETRIES
from ffm.openai.resources.chat.chat import Chat, AsyncChat
from openai._streaming import Stream, AsyncStream

_deployments_endpoints = set(
    [
        "/conversation",        
        "/embeddings"        
    ]
)

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])

class BaseFfmClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    """台智雲基礎用戶端類別"""

    @override
    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        """建立httpx的請求物件
        
        Args:
            options (FinalRequestOptions): 最終請求參數

        Returns:
            httpx.Request: 請求物件
        """
        if options.url in _deployments_endpoints and is_mapping(options.json_data):
            model = options.json_data.get("model")
            if model is not None:
                options.url = f"/models{options.url}"

        return super()._build_request(options)

class FfmOpenAI(BaseFfmClient[httpx.Client, Stream[Any]], OpenAI):
    """台智雲OpenAI相容同步用戶端

    Args:
        BaseFfmClient (_type_): _description_
        OpenAI (_type_): _description_
    """

    chat: Chat
    """覆寫OpenAI原本的chat completions類別"""

    def __init__(
        self, 
        *,
        api_url: str,
        api_key: str,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None        
    ):        
        """初始化FfmOpenAI物件

        Args:
            api_url (str): 台智雲端點網址，結尾必須是API，如果是public模型，網址是https://api-ams.twcc.ai/api
            api_key (str): API金鑰.
            timeout (float | Timeout | None | NotGiven, optional): 逾時設定. Defaults to NOT_GIVEN.
            max_retries (int, optional): 最大重試次數. Defaults to DEFAULT_MAX_RETRIES.
            http_client (httpx.Client | None, optional): HTTP用戶端. Defaults to None.
        """
        base_url = f"{api_url}"        

        super().__init__(            
            api_key=api_key,
            base_url = base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers={
                'X-API-HOST': "afs-inference", # 如果呼叫public端點需要加上x-api-host，私有端點不需要，目前先固定加上
                "content-type": "application/json",
                "X-API-KEY": api_key
            },
            http_client=http_client
        )       

        self.chat = Chat(self)

class AsyncFfmOpenAI(BaseFfmClient[httpx.AsyncClient, AsyncStream[Any]], AsyncOpenAI):
    """台智雲OpenAI相容非同步用戶端"""
    
    chat: AsyncChat
    """覆寫OpenAI原本的chat completions類別"""

    def __init__(
        self,
        *,
        api_url: str,
        api_key: str,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None        
    )-> None:
        """初始化AsyncFfmOpenAI物件

        Args:
            api_url (str): 台智雲端點網址，結尾必須是API，如果是public模型，網址是https://api-ams.twcc.ai/api
            api_key (str): API金鑰.
            timeout (float | Timeout | None | NotGiven, optional): 逾時設定. Defaults to NOT_GIVEN.
            max_retries (int, optional): 最大重試次數. Defaults to DEFAULT_MAX_RETRIES.
            http_client (httpx.Client | None, optional): HTTP用戶端. Defaults to None.
        """
        base_url = f"{api_url}"        

        super().__init__(            
            api_key=api_key,
            base_url = base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers={
                'X-API-HOST': "afs-inference",
                "content-type": "application/json",
                "X-API-KEY": api_key
            },
            http_client=http_client
        )

        self.chat = AsyncChat(self)