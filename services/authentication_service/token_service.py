from utils import util_funcs
from decouple import config
from cores.authen import signJWT, decodeJWT

class TokenService():
    def __init__(self, uid=None, token=None):
        self.uid = uid
        self.token = token
    
    def generate_user_token(self, long_live=False):
        if long_live:
            duration = config('USER_ACCESS_TOKEN_LONG_LIVE')
            expires_at = util_funcs.create_expires_duration(days=duration)
        else:
            duration = config('USER_ACCESS_TOKEN_SHORT_LIVE')
            expires_at = util_funcs.create_expires_duration(seconds=duration)
        info = util_funcs.token_user_access_format(id=self.uid, expires_at=expires_at)
        return signJWT(info=info)

    def get_uid_from_token(self):
        try:
            payload = decodeJWT(token=self.token)
            return payload['uid']
        except Exception:
            return None