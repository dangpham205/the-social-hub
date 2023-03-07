import datetime
from functools import wraps
from cores.authen.auth_handler import decodeJWT
from services.authentication_service import TokenService

def refresh_token(func):
    @wraps(func)
    async def wrap_func(*args, **kwargs):
        result = await func(*args, **kwargs)

        try:
            token = kwargs['user_token'] 
            payload = decodeJWT(token=token)
            expires_at = payload['expires_at']
            now = datetime.datetime.now()
            expires_at = datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S.%f')
            delta = expires_at-now
            total_minutes = int(delta.total_seconds() / 60)
            if 0 < total_minutes < 20:
                new_token = TokenService(uid=payload['uid']).generate_user_token()
                result.token = new_token
                result['token'] = new_token
            else:
                result['token'] = None
        except:
            pass
        return result

    return wrap_func