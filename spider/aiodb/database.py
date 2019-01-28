import aiosqlite


class DatabaseSession(object):
    def __init__(self, path):
        self._path = path

    async def __aenter__(self): 
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None
    
    async def _select(self,
                      sql_command: str,
                      values: tuple,
                      many: bool = False) -> [tuple, None]:
        async with aiosqlite.connect(self._path) as db:
            cursor = await db.execute(sql_command, values)

            if many:
                rows = await cursor.fetchall()
            else:
                rows = await cursor.fetchone()

            await cursor.close()

        return rows

    async def _insert(self,
                      sql_command: str,
                      values: tuple) -> int:
        async with aiosqlite.connect(self._path) as db:
            cursor = await db.execute(sql_command, values)
            row_id = cursor.lastrowid

            await db.commit()
            await cursor.close()
            return row_id

    async def create_tables(self):
        async with aiosqlite.connect(self._path) as db:
            sql_script = '''
            CREATE TABLE url_relations
            (id INTEGER PRIMARY KEY,
             page_id INTEGER NOT NULL,
             parent_id INTEGER DEFAULT NULL);
            CREATE TABLE pages
            (id INTEGER PRIMARY KEY,
             url TEXT NOT NULL,
             html TEXT NOT NULL);
            '''
            await db.executescript(sql_script)
            await db.commit()

    async def has_url(self, url: str) -> bool:
        if await self.get_page_id(url):
            return True
        else:
            return False

    async def get_page_id(self, url: str) -> [int, None]:
        sql_command = 'SELECT id FROM pages WHERE url=?'
        values = (url,)
        page_id = await self._select(sql_command, values)
        if page_id:
            return page_id[0]
        else:
            return None

    async def insert_relation(self, page_id: int, parent_id: int):
        sql_command = '''
        INSERT INTO url_relations (page_id, parent_id)
        VALUES (?,?)
        '''
        values = (page_id, parent_id,)
        await self._insert(sql_command, values)

    async def insert_page(self, url: str, html: str) -> int:
        async with aiosqlite.connect(self._path) as db:
            page_sql_command = '''
            INSERT INTO pages (url, html)
            VALUES (?,?)
            '''
            values = (url, html,)

            page_id = await self._insert(page_sql_command,
                                         values)
            return page_id
