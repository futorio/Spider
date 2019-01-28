from database import DatabaseSession
import asyncio

async def main():
    db_session = DatabaseSession('test.db')
    if await db_session.has_url('hello'):
        url_id, html = await db_session.get_content_id('hello')
        print([url_id, html[:5]])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
