import json
import os
from click import Option
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain.embeddings.base import Embeddings

class FFMEmbeddings(BaseModel, Embeddings):
    base_url: str = "https://api-ams.twcc.ai/api"
    api_key: str = ""
    chunk_size: int = 1000
    max_retries: int = 2
    request_timeout: Optional[Union[float, Tuple[float, float], Any]] = Field(default=None, alias="timeout")
    model: Optional[str] = Field(default="ffm-embedding", title="Embedding model name, default is 'ffm-embedding'")
    headers: Dict[str, str] = Field(default_factory=dict)

    class Config:
        """Configuration for this pydantic object."""
        extra = "forbid"
        allow_population_by_field_name = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key exists in environment."""
        api_key = values.get("api_key") or os.getenv("FFM_API_KEY")
        if not api_key:
            raise ValueError("API key must be provided either as a parameter or an environment variable FFM_API_KEY")
        values["api_key"] = api_key
        return values

    def _get_embeddings(self, payload: str) -> List[List[float]]:
        """Helper method to get embeddings from the API."""
        endpoint_url = f"{self.base_url}/models/embeddings"
        headers = {
            "Content-type": "application/json",            
            "X-API-KEY": self.api_key,
            "X-API-HOST": "afs-inference",
            **self.headers
        }
        for _ in range(self.max_retries):
            payload_dict = {

            }
            response = requests.post(endpoint_url, headers=headers, data=payload, timeout=self.request_timeout)
            if response.status_code == 200:
                body = response.json()
                return [data["embedding"] for data in body["data"]]
            elif response.status_code == 429:  # Rate limit error
                continue
            else:
                response.raise_for_status()
        raise RuntimeError("Failed to get embeddings after maximum retries")

    def embed_documents(self, texts: List[str], chunk_size: Optional[int] = None) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        chunk_size = chunk_size or self.chunk_size
        embeddings: List[List[float]] = []
        for i in range(0, len(texts), chunk_size):
            payload = json.dumps({"model": self.model, "inputs": texts[i:i+chunk_size]})
            embeddings.extend(self._get_embeddings(payload))
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query."""
        return self.embed_documents([text])[0]
    
    async def aembed_documents(self, texts: List[str], chunk_size: Optional[int] = None) -> List[List[float]]:
        """Generate embeddings for a list of documents asynchronously."""
        chunk_size = chunk_size or self.chunk_size
        embeddings: List[List[float]] = []
        for i in range(0, len(texts), chunk_size):
            payload = json.dumps({"model": self.model, "inputs": texts[i:i+chunk_size]})
            embeddings.extend(await self._aget_embeddings(payload))
        return embeddings

    async def aembed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query asynchronously."""
        embeddings = await self.aembed_documents([text])
        return embeddings[0]
