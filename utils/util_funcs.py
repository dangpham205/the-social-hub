import datetime


def return_status_codes(*args):
    return f'Return status codes: {args}'

def create_expires_duration(seconds=None, days=None):
    if seconds:
        return datetime.datetime.now() + datetime.timedelta(seconds = int(seconds))
    if days:
        return datetime.datetime.now() + datetime.timedelta(days = int(days))
    return datetime.datetime.now() + datetime.timedelta(seconds = int(3600))
    

def token_signup_format(id, expires_at):
    return {
        'uid': id,
        'expires_at': expires_at.isoformat()
    }

def token_user_access_format(id, expires_at):
    return {
        'uid': id,
        'expires_at': expires_at.isoformat()
    }
    