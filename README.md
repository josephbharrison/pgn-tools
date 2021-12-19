# pgn-tools
Chess tools for downloading, parsing, and searching PGN files.
### Download TWIC PGN files
```shell
$ ./dl-twic.sh 920 1414
```
### Search PGN
```sh
$ python3 -m search -h
search usage:
    -f, --file <string>        [mandatory] PGN file (ex: "pgn/twic1368.pgn")
    -h, --help                 Print usage
    -p, --player <string>      Player name (white or black)
    -w, --white <string>       White player name
    -b, --black <string>       Black player name
    -r, --result <str>         Game result: (1-0, 0-1, 1/2-1/2)
    -e, --eco <string>         ECO opening name
    -o, --opening <string>     Opening name
    -V, --variation <string>   Opening variation name
    -E, --event <string>       Event name
    -s, --site <string>        Site (location)
    -d, --game_date <date>     Date of game (format: "YYYY.MM.DD")
    -D, --event_date <date>    Date of event (format: "YYYY.MM.DD")
    --date_min <date>          Minimum date (format: "YYYY.MM.DD")
    --date_max <date>          Maximum date (format: "YYYY.MM.DD")
    --elo_min <int>            Minimum elo rating
    --elo_max <int>            Maximum elo rating
```
Examples:
```shell
# Find Caruana games with Elo ratings 2700 or higher in twic1368.pgn
$ python3 -m search -p Caruana --elo_min 2700 -f pgn/twic1368.pgn

# Create new PGN file from 2300 or higher rated games
$ for file in pgn/twic[0-9]*.pgn; do python3 -m search --elo_min 2300 -f $file >> pgn/twic-elo-2300.pgn; done
```

