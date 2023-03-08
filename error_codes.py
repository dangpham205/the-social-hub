
from enum import Enum

def code_detail(msg, where=True):
    if where:
        where = 'Response Body'
    else:
        where = 'Real Response Status Code'
    return {
        'Detail': msg,
        'Where to find the status code': where,
    }

status_code_dict = {
    401: code_detail("invalid token from user (can't decode)", where=False),
    402: code_detail('expired token from user --> login again', where=False),
    403: code_detail('wrong bearer token (not Header Bearer token, ...)', where=False),
    405: code_detail('token does not have permission to perform the action (Eg: trying to update another user profile)'),
    501: code_detail('write data to mysql failed'),
    502: code_detail('send email failed (confirm signup, ...)'),
    503: code_detail('confirm signup failed (touched token, token is invalid)'),
    504: code_detail('confirm signup expired'),
    505: code_detail('user already verified'),
    506: code_detail('login with unregistered email/username'),
    507: code_detail('wrong password'),
    508: code_detail('unverified user try to login'),
}

def get_code_detail(code: int):
    if code in status_code_dict:
        return status_code_dict[code]
    return 'Không tìm thấy má ơi'

# 501: write data to mysql failed
# 502: send email failed (confirm signup, ...)
# 503: confirm signup failed (touched token, token is invalid)
# 504: confirm signup expired
# 505: user already verified
# 506: login with unregistered email/username
# 507: wrong password
# 508: unverified user try to login



# For all the APIs that required authentication token
#     real status code - 401: invalid token from user (can't decode)
#     real status code - 403: wrong bearer token (not Header Bearer token, ...)
#     real status code - 402: expired token from user --> login again
#     response body status code - 405: token does not have permission to perform the action (trying to update another user profile)
