from openai import OpenAI
from pathlib import Path
import base64
from typing import Optional, Union, BinaryIO

class ImageAPI:
    def __init__(self, api_key: str, base_url: str = "https://www.dmxapi.cn/v1"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    def _encode_image(self, image_path: Union[str, Path, BinaryIO]) -> str:
        if isinstance(image_path, (str, Path)):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            return base64.b64encode(image_path.read()).decode('utf-8')
    
    def generate_image(
        self,
        prompt: str,
        image_path: Optional[Union[str, Path, BinaryIO]] = None,
        model: str = "gpt-4o-image",
        stream: bool = False
    ):
        messages = [{
            "role": "user",
            "content": prompt
        }]
        
        if image_path:
            if 'http' in image_path:
                messages[0]["content"] = [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": image_path}
                ]
            else:
                base64_image = self._encode_image(image_path)
                messages[0]["content"] = [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
        
        return self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=stream
        )
