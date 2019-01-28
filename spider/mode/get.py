import sqlite3
import os
from htmlParser import get_title


class GetSession(object):
    def __init__(self, db_path: str, root_url: str, n: int, html_path: str):
        self._db_path = db_path
        self._root_url = root_url
        self._n = n
        self._html_path = html_path

    def save_html(self, html: str, name: str):
        path = os.path.abspath(f'{self._html_path}/{name}.html')
        with open(path, 'w') as html_file:
            html_file.write(html)

    def show_pages(self):

        if not os.path.exists(self._db_path):
            print(f'database path "{self._db_path}" does not exist')
            return None

        if (self._html_path is not None) and (not os.path.exists(self._html_path)):
            print(f'directory "{self._html_path}" does not exist')
            return None

        sql_command = '''
        SELECT pages.url, pages.html
        FROM pages
        INNER JOIN url_relations ON pages.id = url_relations.page_id
        WHERE url_relations.parent_id = (SELECT pages.id FROM pages WHERE pages.url = ?)
        LIMIT ?
        '''
        values = (self._root_url, self._n,)

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(sql_command, values)
            rows = cursor.fetchall()

            if self._html_path:
                for row, index in zip(rows, range(len(rows))):
                    self.save_html(row[1], index)

            for url, html in rows:
                title = get_title(html)
                print(f'{url}: "{title}"')
