
class authen_admin():
    def __init__(self) -> None:
        pass
    
    # f là function đằng sau decorator khi được gọi
    def __call__(self, f):
        def wrapped(*args, **kwargs):
            # *args là các param của function đuọc define sau decorator
            
            wm = args[0]
            token = wm.user_token
            # vi du ham wm().getListFolder() sẽ có "self" là first param, mà trong wm() thì có "attr user_token"
            # ==> có thể truy cập qua obj "self"
            
            is_admin = self.__verify__(token)
            if is_admin:
                return f(*args, **kwargs)
            else:
                return "Bạn không có quyền"
        return wrapped

    def __verify__(self, token):
        # uid = workers().get_UserID_from_token(token)
        uid = None
        # id account admin hiện tại là 1
        if uid and uid == 1:
            return True
        else:
            return False