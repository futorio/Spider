import aiohttp


async def download_html(url: str, show_errors: bool = False) -> tuple:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                html = await resp.content.read()
                size = len(html)
                return html.decode('utf-8'), size
        except:
            if show_errors:
                print(f'error on url {url}')
            await session.close()
            return None, None

