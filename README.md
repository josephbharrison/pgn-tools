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
    -h, --help              Print usage
    -f, --file <string>     PGN file
    -p, --player <string>   Player name (white or black)
    -w, --white <string>    White player name
    -b, --black <string>    Black player name
    -r, --result <str>      Game result: (1-0, 0-1, 1/2-1/2)
    --elo_min <int>         Minimum elo rating
    --elo_max <int>         Maximum elo rating
```
Example:
```shell
$ python3 -m search -p Caruana --elo_min 2700 -f pgn/twic1368.pgn
```
