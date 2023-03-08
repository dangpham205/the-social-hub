import datetime
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    """_summary_

    Args:
        HTTPBearer (_type_): _description_
    Desc:
        Lớp này chịu trách nhiệm thực thi việc kiểm tra tính hợp lệ của người dùng khi nhận được yêu cầu thực hiện tính năng
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        """Được gọi trước khi thực hiện request"""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        # obj(scheme='Bearer' credentials='token that got from api call')

        if credentials:
            
            if not credentials.scheme == "Bearer": # kiểm tra tính đúng đắn theo chuẩn Bearer
                raise HTTPException(status_code=403, detail='Invalid authentication scheme')
            
            verify_token = self.verify_jwt(credentials.credentials) # kiểm tra token
            if verify_token == False:
                raise HTTPException(status_code=401, detail='Invalid token')
            if verify_token == None:
                raise HTTPException(status_code=402, detail='Expired token')
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403,detail='Invalid authorization code.')
        
    # cần bổ sung thêm thông số của request để nhận biết url nào đang được gọi đến
    def verify_jwt(self,jwtoken: str)->bool:
        # False: token can't be decoded
        # None: token expired --> proceed with login
        # True: OK 
        payload = decodeJWT(token=jwtoken)
        try:
            expires_at = payload['expires_at']
            now = datetime.datetime.now()
            expires_at = datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S.%f')
            if now > expires_at: 
                return None
            return payload
        except:
            return payload
