from pythondi import Provider, configure
# from repositories.contracts.school_contract import SchoolContract
# from repositories.sqlachemy.school_repository import SchoolRepository


"""
    Khỏi tạo dependency injection
    Quyết định class nào sẽ được thực thi khi implement từ interface
"""
def init_di():
    provider = Provider()
    # provider.bind(SchoolContract, SchoolRepository)
    # provider.bind(SqlAchemyContracts, SqlAchemyAbstract)
    configure(provider=provider)
