
class refresh_token():
    def __init__(self) -> None:
        pass
    
    # f là function đằng sau decorator khi được gọi
    def __call__(self, f):
        async def wrapper():
            response = await f()
            response['status'] = 'success'
            return response
        return wrapper
        async def wrapped():
        # def wrapped(*args, **kwargs):
            
            # wm = args[0]
            # token = wm.user_token
            print(0)
            # print(kwargs)
            # is_admin = self.__verify__(token)
            # if is_admin:
            # return f(*args, **kwargs)
            response =  await f()
            if type(response) == dict:
                response['dqưe'] = 'rtrtrtr'
            return response
            # else:
            #     return "Bạn không có quyền"
        return wrapped

    def __verify__(self, token):
        # uid = workers().get_UserID_from_token(token)
        uid = None
        # id account admin hiện tại là 1
        if uid and uid == 1:
            return True
        else:
            return False