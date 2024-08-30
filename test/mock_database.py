from src.database import IDatabase
from typing import List

class MockDatabase(IDatabase):
    def __init__(self):
        self.queries = []

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def create_tables(self):
        pass

    async def save_query(self, domain: str, ip_addresses: List[str]):
        self.queries.append({"domain": domain, "ip_addresses": ip_addresses})

    async def get_latest_queries(self, limit: int):
        return self.queries[-limit:]