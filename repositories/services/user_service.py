from pythondi import inject
from repositories.contracts.user_contract import UserContract
class UserService:
    @inject()
    def __init__(self, repo: UserContract):
        print('user_service')
        self.repo = repo
