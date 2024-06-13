from datetime import timedelta  
import datetime  
from jose import jwt  
from jose.exceptions import ExpiredSignatureError, JWTError  
import binascii
from fastapi import Request
from fastapi.responses import JSONResponse

class JWTUtils:  
    def __init__(self, access_key_secret="e325663645455784e444e6364", expires_in=86400):  
        self.access_key_secret = access_key_secret  
        self.expires_in = expires_in  
  
    def encode_token(self, data: dict):  
        expire = datetime.datetime.now() + timedelta(seconds=self.expires_in)  
        to_encode = dict({"exp": expire}, **data)  
        token = jwt.encode(to_encode, self.access_key_secret, algorithm="HS256")  
        token = binascii.hexlify(token.encode())
        return token  
  
    def decode_token(self, token: str):  
        try:  
            # 假设您在这里去除token的前缀（例如Bearer ）是因为您的token是以"Bearer "开头的  
            # 但这通常取决于您的具体实现和前端如何发送token  
            token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token  
            token = bytes.fromhex(token).decode()
            payload = jwt.decode(token, self.access_key_secret, algorithms="HS256")  
            return payload  
        except (ExpiredSignatureError, JWTError) as e:  
            print(e) 
            return None  
  
    def auth_user(self, headers):  
        token = headers.get("Authorization") 
        payload = self.decode_token(token)  
        return payload  
  
class TokenMiddleware:  
    def __init__(self, access_key_secret="e325663645455784e444e6364", expires_in=86400, white_list=["/token"], white_method=["GET"]) -> None:
        self.jwt = JWTUtils(access_key_secret, expires_in)
        self.white_list = white_list
        self.white_method = white_method

    async def token_validation_middleware(self,request: Request, call_next):
        if request.url.path not in self.white_list and request.method.upper() not in self.white_method:
            token = request.headers.get("Authorization")
            if token:
                try:
                    res = self.jwt.decode_token(token)
                    if not res:
                        return JSONResponse(
                            content={"errorcode": "9001", "message": "token error"},
                            status_code=401,
                        )
                except Exception as e:  # 处理解码可能出现的异常
                    return JSONResponse(
                        content={
                            "errorcode": "9001",
                            "message": "token decode error: " + str(e),
                        },
                        status_code=401,
                    )
            else:
                return JSONResponse(
                    content={"errorcode": "9001", "message": "token not found"},
                    status_code=401,
                )
        return await call_next(request)