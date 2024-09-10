import logging
import asyncpg
from src.settings import settings
from abc import ABC, abstractmethod
from typing import List
import asyncio


class IDatabase(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def create_tables(self):
        pass

    @abstractmethod
    async def save_query(self, domain: str, ip_addresses: List[str]):
        pass

    @abstractmethod
    async def get_latest_queries(self, limit: int):
        pass


logger = logging.getLogger(__name__)


class Database(IDatabase):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'pool'):
            self.pool = None

    async def connect(self):
        retries = 3
        for attempt in range(retries):
            try:
                self.pool = await asyncpg.create_pool(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                )
                logger.info("Database pool initialized connection")
                break
            except asyncpg.PostgresError as e:
                logger.error(f"Error connecting to database: {e}")
                if attempt < retries - 1:
                    logger.info(f"Retrying connection attempt {attempt + 1}/{retries}")
                    await asyncio.sleep(3)
                else:
                    logger.error("Failed to connect to database after multiple attempts")
                    raise

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
        logger.info("Database connection closed")

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id SERIAL PRIMARY KEY,
                    domain TEXT NOT NULL,
                    ip_addresses TEXT[] NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT
                    CURRENT_TIMESTAMP
                )
            ''')
        logger.info("Database table created")

    async def save_query(self, domain, ip_addresses):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO queries (domain, ip_addresses) VALUES ($1, $2)",
                domain, ip_addresses
            )
        logger.info("DNS query saved")

    async def get_latest_queries(self, limit):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT domain, ip_addresses, created_at FROM queries "
                "ORDER BY created_at DESC LIMIT $1", limit
            )
            return [dict(row) for row in rows]
