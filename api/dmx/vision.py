from .client import DMXAPIClient
from typing import Union

class VisionAPI(DMXAPIClient):
    """多模态图像分析接口"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "v1/chat/completions"
    
    def analyze_image(
        self,
        image_url: str,
        prompt: str,
        model: str = "gemini-2.0-flash-thinking-exp-1219",
        temperature: float = 0.1
    ) -> str:
        """分析图像内容"""
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "temperature": temperature
        }
        
        response = self._send_request("POST", self.endpoint, payload)
        print(response)
        return self.parse_response(response)
