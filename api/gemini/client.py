import os
import mimetypes
from typing import Optional, Dict, Any
from google.genai import Client as GenAI_Client, types
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import base64

class GeminiAPIClient:
    """GeminiAPI 基础客户端"""
    
    def __init__(
        self,
        api_key: str,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: tuple = (429, 500, 502, 503, 504),
        timeout: int = 2000
    ):
        self.api_key = api_key
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.timeout = timeout
        self.client = GenAI_Client(api_key=api_key)
        self._configure_session()
    
    def _configure_session(self):
        """配置带超时和自动重试的Session"""
        session = requests.Session()
        retries = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        # 注意：这里假设GenAI_Client内部使用了requests.Session，如果实际没有，则此部分需要调整
        # 如果GenAI_Client不使用requests.Session，你可能需要在这里添加其他逻辑来应用重试策略
    
    def generate_image_from_prompt(
        self,
        prompt: str,
        image_paths: list[str],
        model_name: str = "gemini-2.0-flash-exp-image-generation",
        temperature: float = 1.0
    ) -> Optional[str]:
        """
        根据提示词和输入图片生成新图片
        ...（保留原有文档字符串）
        """
        try:
            # 上传文件
            uploaded_file = self._upload_with_retry(image_paths)
            # 构建请求内容
            contents = self._build_contents(uploaded_file, prompt)
            
            # 生成配置
            config = self._build_generate_config(temperature)
            
            # 流式生成并保存图片
            return self._generate_and_save_image(model_name, contents ,config)
        
        except Exception as e:
            raise RuntimeError(f"生成过程中发生错误: {str(e)}") from e
    
    def _read_images_as_base64(self, image_paths: list[str]) -> Dict[str, str]:
        """读取本地图片文件并转换为Base64编码"""
        base64_images = {}
        for image_path in image_paths:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"输入图片不存在: {image_path}")
            with open(image_path, "rb") as f:
                file_data = f.read()
                base64_encoded = base64.b64encode(file_data).decode('utf-8')
                mime_type, _ = mimetypes.guess_type(image_path)
                base64_images[image_path] = (mime_type, base64_encoded)
        return base64_images

    def _upload_with_retry(self, image_paths: list[str]) -> list[Dict[str, Any]]:
        """带重试机制的文件上传，支持多张图片"""
        uploaded_files = []
        base64_images = self._read_images_as_base64(image_paths)
        for attempt in range(self.max_retries):
            try:
                for path, (mime_type, base64_data) in base64_images.items():
                    uploaded_files.append(
                        types.Part.from_bytes(
                            mime_type=mime_type,
                            data=base64.b64decode(base64_data)  # 确保数据是bytes类型
                        )
                    )
                
                break  # 如果上传成功，则跳出循环
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError("文件上传失败") from e
        return uploaded_files
    
    def _build_contents(self, uploaded_file: Any, prompt: str) -> Dict[str, Any]:
        """构建请求内容"""

        return [
            types.Content(
                role="user",
                parts=[
                    *uploaded_file,
                    types.Part.from_text(text=prompt),
                ],
            )
        ]
    
    def _build_generate_config(self, temperature: float) -> types.GenerateContentConfig:
        """构建生成配置"""
        return types.GenerateContentConfig(
            temperature=temperature,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_modalities=["image", "text"],
           response_mime_type="text/plain",
        )
    
    def _generate_and_save_image(self, model_name: str, contents: Dict[str, Any], config: types.GenerateContentConfig) -> Optional[str]:
        """流式生成并保存图片"""
        for chunk in self.client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
            
        ):
            if chunk.candidates and chunk.candidates[0].content.parts:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                    # 假设 inline_data.data 是 str 类型
            if isinstance(inline_data.data, str):
                byte_data = inline_data.data.encode('utf-8')  # 转换为 bytes
            elif isinstance(inline_data.data, (bytes, bytearray)):
                byte_data = inline_data.data  # 如果已经是 bytes 或 bytearray 类型，则无需转换
            else:
                # 对于其他类型，考虑是否需要转换或序列化为 bytes
                # 这里以简单的 str() 和 encode() 方法为例，但可能需要根据实际情况调整
                byte_data = str(inline_data.data).encode('utf-8')
                return inline_data.data
        return byte_data

# 自定义异常类（如果需要）
class APIError(Exception):
    """自定义API异常"""
    pass

class ResponseParseError(Exception):
    """响应解析异常"""
    pass
