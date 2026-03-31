import asyncpg
from typing import List, Dict


class TermoContratualRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def get_all(self) -> List[Dict]:
        query = "SELECT id, nome FROM termo_contratual ORDER BY nome"
        rows = await self.conn.fetch(query)
        return [dict(r) for r in rows]
