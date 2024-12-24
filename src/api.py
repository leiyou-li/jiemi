from   从 fastapi import   进口 FastAPI, HTTPException
from pydantic import BaseModel
from .decrypt_service import URLDecryptService

app = FastAPI(title="URL解密服务")
decrypt_service = URLDecryptService()

class URLRequest(BaseModel):
    url: str

@app.post("/decrypt")
async def decrypt_url(request: URLRequest):
    """
    解密URL接口
    """
    result = decrypt_service.decrypt_url(request.url)
    if result is None:
        raise HTTPException(status_code=400, detail="解密失败")
    return {"result": result}

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"} 

