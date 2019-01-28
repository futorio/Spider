import re


def get_links(html: str) -> list:
    reg_exp = r'href="https?.+?\/"'
    unique_urls = set()

    for unf_url in re.findall(reg_exp, html):
        url = unf_url.split(sep='"')[1]
        unique_urls.add(url)

    return list(unique_urls)


def get_title(html: str) -> str:
    reg_exp = r'<title[^>]*>(.*?)</title>'
    html_title = re.findall(reg_exp, html)
    if html_title:
        return html_title[0]
    else:
        return 'NOTITLE'
