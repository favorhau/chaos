import json
import time
import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DMXAPIClient:
    """DMXAPI 基础客户端"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://www.dmxapi.cn",
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        
        # 配置带超时和自动重试的Session
        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # 通用请求头
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "DMXAPI-Client/1.0.0 (Python)"
        }
    
    def _send_request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """发送基础请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                data=json.dumps(payload) if payload else None,
                timeout=self.timeout
            )
            print(response.raw.read())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # 更具体的错误处理
            error_info = {
                "status_code": e.response.status_code,
                "error_message": f"HTTP Error: {str(e)}",
                "response_text": e.response.text[:200]  # 截取部分错误内容
            }
            raise APIError(error_info)
        except requests.exceptions.RequestException as e:
            error_info = {
                "error_message": f"Request failed: {str(e)}"
            }
            raise APIError(error_info)
    
    def parse_response(self, response: Dict, result_key: str = "choices") -> Any:
        """通用响应解析"""
        if not isinstance(response, dict):
            raise ResponseParseError("Invalid response format")
            
        if "data" in response:
            return response["data"]
        if result_key in response:
            return response[result_key][0].get("message", {}).get("content", "")
        return response

class APIError(Exception):
    """自定义API异常"""
    def __init__(self, error_info: dict):
        self.error_info = error_info
        super().__init__(json.dumps(error_info))

class ResponseParseError(Exception):
    """响应解析异常"""
