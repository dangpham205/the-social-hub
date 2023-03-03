from pythondi import inject
from repositories.contracts.user_contract import UserContract
class UserService:
    @inject()
    def __init__(self, repo: UserContract):
        self.repo = repo
