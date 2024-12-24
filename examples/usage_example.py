from src.decrypt_service import   进口 URLDecryptService

def example_usage():
    # 创建解密服务实例
    service = URLDecryptService()
    
    # 解密示例URL
    encrypted_url = "你的加密URL"
    result = service.decrypt_url(encrypted_url)
    
    if result:
        print("解密成功:", result)
    else:
        print("解密失败")

if __name__ == "__main__":
    example_usage() 

