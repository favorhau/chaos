from .client import DMXAPIClient
from typing import List

class EmbeddingAPI(DMXAPIClient):
    """文本向量化接口"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "v1/embeddings"
    
    def get_embedding(
        self, 
        text: str,
        model: str = "text-embedding-ada-002"
    ) -> List[float]:
        """获取文本向量"""
        
        payload = {
            "input": text,
            "model": model
        }
        
        response = self._send_request("POST", self.endpoint, payload)
        return response.get("data", [{}])[0].get("embedding", [])
