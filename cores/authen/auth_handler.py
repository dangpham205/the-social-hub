from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

def signJWT(info:dict)->Dict[str,str]:
    payload = info
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token:str)->dict:
    try:
        decode_token = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        return decode_token #if decode_token['expires']>= time.time() else None
    except:
        return False

if __name__ == '__main__':
    token = signJWT('tui@abc.com')
    print(token)