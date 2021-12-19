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
Examples:
```shell
# Find Caruana games with Elo ratings 2700 or higher in twic1368.pgn
$ python3 -m search -p Caruana --elo_min 2700 -f pgn/twic1368.pgn

# Create new PGN file from 2300 or higher rating games
$ for file in pgn/twic[0-9]*.pgn; do python3 -m search --elo_min 2300 -f $file >> pgn/twic-elo-2300.pgn; done
```
