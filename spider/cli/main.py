import argparse


argParser = argparse.ArgumentParser(
    prog='spider',
    description='simple asynchronous site parser')

argParser.add_argument('mode',
                       help='"load" for start recursive download, "get" to get n urls and titles (use -n key)',
                       choices=['load', 'get'],
                       type=str)

argParser.add_argument('-n',
                       help='amount of child pages',
                       type=int)

argParser.add_argument('url',
                       help='url for download or get child pages',
                       type=str)

argParser.add_argument('--depth',
                       help='download depth. Start with 0',
                       type=int,
                       default=0)

argParser.add_argument('--html-path',
                       help='path to save html from get urls')

argParser.add_argument('--db-path',
                       help='path to database if database does not exist create')

argParser.add_argument('--show-errors',
                       help='show any error messages',
                       default=False)


def get_args():
    return argParser.parse_args()
