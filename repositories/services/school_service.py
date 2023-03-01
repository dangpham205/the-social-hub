from pythondi import inject
from repositories.contracts.school_contract import SchoolContract
class SchoolService:
    @inject()
    def __init__(self, repo: SchoolContract):
        self.repo = repo
