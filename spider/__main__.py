from cli import get_args
from mode import LoadSession, GetSession
#from mode import GetSession

arguments = get_args()

if arguments.mode == 'load':
    ld_session = LoadSession(arguments.db_path, arguments.show_errors)
    ld_session.create_db()
    total_time, total_size = ld_session.run(arguments.url, arguments.depth)
    print(f'ok, execution time: {total_time}s, memory usage: {total_size//10**6} Mb')

elif arguments.mode == 'get':
    get_session = GetSession(arguments.db_path, arguments.url, arguments.n, arguments.html_path)
    get_session.show_pages()

