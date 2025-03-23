from .client import DMXAPIClient
from typing import Union
import base64

class VisionAPI(DMXAPIClient):
    """多模态图像分析接口"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "v1/chat/completions"
    
    def encode_image(self, image_path: str) -> str:
        """
        读取本地图片并编码为Base64字符串。
        
        Args:
            image_path (str): 本地图片路径。
        
        Returns:
            str: Base64编码的图片字符串。
        
        Raises:
            FileNotFoundError: 如果图片文件不存在。
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_string
        except FileNotFoundError:
            raise FileNotFoundError(f"图片文件未找到: {image_path}")
        
    def analyze_image(
        self,
        image_source: Union[str, dict],
        source_type: str,  # 使用字符串标识来源
        prompt: str,
        model: str = "gemini-2.0-flash-thinking-exp-1219",
        temperature: float = 0.1
    ) -> str:
        """分析图像内容"""
        
        if source_type == "url":
            # 处理图片URL
            image_url = {"url": image_source}
        elif source_type == "local":
            # 处理Base64编码的本地图片
            if isinstance(image_source, str):
                base64_image = self.encode_image(image_source)
                image_url = {"url": f"data:image/png;base64,{base64_image}"}
            elif isinstance(image_source, dict) and "url" in image_source:
                image_url = image_source
            else:
                raise ValueError("当source_type为local时，image_source必须是本地图片路径字符串或包含Base64编码的字典")
        else:
            raise ValueError("未知的source_type")
        
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
