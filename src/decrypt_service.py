import requests
import json
import time
import logging
from urllib.parse import urlparse
from typing import Optional, Dict, Union

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class URLDecryptService:
    """URL解密服务类"""
    
    def __init__(self, base_url: str = "https://api.lige.chat/ua", timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://lige.chat',
            'referer': 'https://lige.chat/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """验证URL格式是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def decrypt_url(self, encrypted_url: str) -> Optional[Union[str, Dict]]:
        """
        解密URL
        
        Args:
            encrypted_url: 需要解密的URL
            
        Returns:
            解密后的结果或None（如果解密失败）
        """
        if not self.is_valid_url(encrypted_url):
            logger.error("无效的URL格式")
            return None
            
        payload = {"url": encrypted_url}
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"尝试第 {attempt + 1} 次解密...")
                logger.debug(f"发送请求: {self.base_url}")
                
                response = requests.post(
                    self.base_url, 
                    headers=self.headers, 
                    json=payload, 
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                
                if not response.text.strip():
                    raise ValueError("收到空响应")
                
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return response.text
                
            except requests.exceptions.Timeout:
                logger.error("请求超时")
                if attempt == self.max_retries - 1:
                    return None
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"{self.max_retries}次尝试后失败: {e}")
                    return None
                logger.warning(f"第{attempt + 1}次尝试失败: {e}")
                logger.info("1秒后重试...")
                time.sleep(1)
            except Exception as e:
                logger.error(f"意外错误: {e}")
                return None 