from typing import Any
from openai import BaseModel
from openai.types.completion_usage import CompletionUsage


class FfmChatCompletionChunk(BaseModel):    
    """
    為台智雲模型設定的串流回應片段類別，參考openai.types.chat.chat_completion_chunk.ChatCompletionChunk
    """

    generated_text: str
    """產生的文字內容

    Returns:
        str: 產生的文字內容
    """

    function_call: Any
    """Function call的內容部分，尚未完整實作接收端，所以用Any接收任何內容

    Returns:
        Any: 任意的function_call欄位回應
    """

    details: Any
    """如果回應有發生例外，會顯示在這裡

    Returns:
        Any: 例外的內容，不確定是什麼型別
    """

    total_time_taken: str
    """單個token回應花費的時間，以"n sec"表示

    Returns:
        str: 單個token回應花費的時間，以"n sec"表示
    """

    prompt_tokens: int
    """花費的輸入提示詞token數量，只會在流式輸出的最後一筆資料中出現

    Returns:
        int: 花費的輸入提示詞token數量
    """

    generated_tokens: int
    """產出的輸出提示詞token數量，只會在流式輸出的最後一筆資料中出現

    Returns:
        int: 產出的輸出提示詞token數量
    """

    total_tokens: int
    """輸入與輸出的提示詞token數量加總，只會在流式輸出的最後一筆資料中出現

    Returns:
        int: 輸入與輸出的token數量加總
    """

    finish_reason: str
    """輸出結束的原因，可能是"length"表示已達設定的最大輸出token數，或是"stop_sequence"是遇到停止字元結束輸出

    Returns:
        str: 輸出結束的原因
    """

    @property
    def usage(self) -> CompletionUsage:
        """為了相容於OpenAI的標準輸出，因此採用property的方式轉換token使用量的資訊

        Returns:
            CompletionUsage: OpenAI的標準輸出格式
        """
        return CompletionUsage(
            prompt_tokens=self.prompt_tokens,
            completion_tokens=self.generated_tokens,
            total_tokens=self.total_tokens
        )