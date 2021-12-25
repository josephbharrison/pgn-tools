# pgn-tools
Chess tools for downloading, parsing, and searching PGN files.
### Download TWIC PGN files
```shell
dl-twic
```
### Generate ECO from PGN
```shell
mk-eco
```
### Search PGN
```sh
search-pgn
```
Usage
```
search-pgn usage:
    -f, --file <string>        [mandatory] PGN file (ex: "pgn/twic1368.pgn")
    -h, --help                 Print usage
    -p, --player <string>      Player name (white or black)
    -w, --white <string>       White player name
    -b, --black <string>       Black player name
    -t, --team <string>        Team name (white or black)
    -F, --fide_id <string>     FIDE Id (white or black)
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
    --white_team <string>      White team name
    --black_team <string>      Black team name
    --white_fide_id <string>   White FIDE Id
    --black_fide_id <string>   Black FIDE Id
```
### Examples:
```shell
# Download all TWIC
$ ./dl-twic

# Download TWIC 920-1414
$ ./dl-twic 920 1414

# Download TWIC 1415
$ ./dl-twic 1415

# Generate ECO from all TWIC
$ ./mk-eco

# Update ECO files from TWIC 1415
$ ./mk-eco pgn/twic/1415.pgn

# Find Caruana games with Elo ratings 2700 or higher in twic1368.pgn
$ ./search-pgn -p Caruana --elo_min 2700 -f pgn/twic/twic1368.pgn

# Create new PGN file from 2300 or higher rated games
$ for file in pgn/twic/twic[0-9]*.pgn; do ./search-pgn --elo_min 2300 -f $file >> pgn/twic-elo-2300.pgn; done
```

