from .client import DMXAPIClient, APIError
from typing import List, Dict, Optional

class ChatAPI(DMXAPIClient):
    """对话生成接口"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "v1/chat/completions"
    
    def create_completion(
        self,
        messages: List[Dict],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        system_prompt: str = "你是一个有帮助的助手",
        **kwargs
    ) -> str:
        """生成文本对话"""
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages
            ],
            "temperature": temperature,
            **kwargs
        }
        
        try:
            response = self._send_request("POST", self.endpoint, payload)
            return self.parse_response(response)
        except APIError as e:
            # 这里可以添加专用错误处理逻辑
            raise
