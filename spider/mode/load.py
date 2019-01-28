from aiodb import DatabaseSession
from htmlParser import get_links
from downloader.main import download_html
import asyncio
import time


class LoadSession(object):
    def __init__(self, _db_path: str, show_errors: bool = False):
        self._main_loop = asyncio.get_event_loop()
        self._db_path = _db_path
        self._show_errors = show_errors
        self.total_size = 0
    
    async def recursive_parse(self, url: str, parent_id: int = None, depth: int = 0):
        async with DatabaseSession(self._db_path) as db_session:
            if await db_session.has_url(url):
                page_id = await db_session.get_page_id(url)
                await db_session.insert_relation(page_id, parent_id)
                return None

        html, size = await download_html(url, self._show_errors)

        if html is None:
            return None

        self.total_size += size
    
        async with DatabaseSession(self._db_path) as db_session:
            page_id = await db_session.insert_page(url, html)
            await db_session.insert_relation(page_id, parent_id)

        if depth > 0:
            for link in get_links(html):
                await self.recursive_parse(link, page_id, depth - 1)
    
    async def _create_db(self):
        async with DatabaseSession(self._db_path) as db_session:
            await db_session.create_tables()

    def create_db(self):
        self._main_loop.run_until_complete(
                self._create_db())

    def run(self, root_url: str, depth: int) -> tuple:
        start = time.time()
        self._main_loop.run_until_complete(
                self.recursive_parse(
                    root_url, 
                    depth=depth)
                )
        total_time = round(time.time()-start)

        return total_time, self.total_size

