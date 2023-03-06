from pythondi import Provider, configure
from repositories.contracts.user_contract import UserContract
from repositories.sqlachemy.user_repository import UserRepository


"""
    Khỏi tạo dependency injection
    Quyết định class nào sẽ được thực thi khi implement từ interface
"""
def init_di():
    print('init di')
    provider = Provider()
    provider.bind(UserContract, UserRepository)
    configure(provider=provider)
