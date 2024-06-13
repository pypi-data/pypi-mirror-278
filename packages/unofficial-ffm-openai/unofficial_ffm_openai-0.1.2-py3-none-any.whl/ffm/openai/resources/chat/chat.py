
from openai._compat import cached_property
from openai._resource import AsyncAPIResource
from ffm.openai.resources.completions import Completions, AsyncCompletions
from openai._resource import SyncAPIResource


class Chat(SyncAPIResource):
    """繼承OpenAI內建的的同步API"""
    
    @cached_property
    def completions(self) -> Completions:
        """Chat Completions的AP要換成台智雲的版本

        Returns:
            Completions: _description_
        """
        return Completions(self._client)

class AsyncChat(AsyncAPIResource):
    """繼承OpenAI內建的"""

    @cached_property
    def completions(self) -> AsyncCompletions:
        """Chat Completions的AP要換成台智雲的版本

        Returns:
            AsyncCompletions: 非同步的Chat Completions類別
        """
        return AsyncCompletions(self._client)