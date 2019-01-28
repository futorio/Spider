# Spider
Simple asynchronous parser

# Instalation
setup in you python env:

    git clone https://github.com/futorio/Spider.git && cd Spider && python3.6 setup.py install
 
 # Usage

    python3.6 -m spider --help
    usage: spider [-h] [-n N] [--depth DEPTH] [--html-path HTML_PATH]
              [--db-path DB_PATH] [--show-errors SHOW_ERRORS]
              {load,get} url

    positional arguments:
      {load,get}            "load" for start recursive download, "get" to get n
                            urls and titles (use -n key)
      url                   url for download or get child pages

    optional arguments:
      -h, --help            show this help message and exit
      -n N                  amount of child pages
      --depth DEPTH         download depth. Start with 0
      --html-path HTML_PATH
                            path to save html from get urls
      --db-path DB_PATH     path to database if database does not exist create
      --show-errors SHOW_ERRORS
                            show any error messages

## Examples
download htmls in database:

      python3.6 -m spider load https://www.vesti.ru/ --db-path 'parsed_content.db' --depth 1

display -n urls|titles:

      python3.6 -m spider get https://www.vesti.ru/ --db-path 'parsed_content.db' -n 5

save(to exist directory!) -n htmls in "--html-path" and display urls|titles: 

      python3.6 -m spider get https://www.vesti.ru/ --db-path 'parsed_content.db' -n 5 --html-path htmls/
