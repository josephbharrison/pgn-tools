import sys
import getopt
import chess.pgn
from common import pgn_load, print_usage, get_options, get_short_opts, get_long_opts, check_mandatory


def search_pgn(
        games: list = None,
        player: str = None,
        white: str = None,
        black: str = None,
        result: str = None,
        elo_min: int = None,
        elo_max: int = None):

    _games = []

    for game in games:
        h = game.headers

        if player:
            if player.lower() not in str(h['Black']).lower() and player not in str(h['White']).lower():
                continue

        if white:
            if white.lower() not in str(h['White']).lower():
                continue

        if black:
            if black.lower() not in str(h['Black']).lower():
                continue

        if result:
            if result != h['Result']:
                continue

        if elo_min:
            if 'WhiteElo' not in h or 'BlackElo' not in h:
                continue

            if elo_min > int(h['WhiteElo']):
                continue

            if elo_min > int(h['BlackElo']):
                continue

        if elo_max:
            if 'BlackElo' not in h or 'WhiteElo' not in h:
                continue

            if elo_max < int(h['WhiteElo']):
                continue

            if elo_max < int(h['BlackElo']):
                continue

        _games.append(game)

    return _games


def main() -> int:
    """
    Search 'main' entrypoint

    :return: exit status
    """

    options = get_options('search')
    short_opts = get_short_opts(options)
    long_opts = get_long_opts(options)

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as err:
        print(err)
        print_usage('search', options)
        return 2

    # option defaults
    player = None
    white = None
    black = None
    result = None
    elo_min = None
    elo_max = None
    file = None

    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage('search', options)
            exit(0)
        elif o in ("-f", "--file"):
            file = a
        elif o in ("-p", "--player"):
            player = a
        elif o in ("-w", "--white"):
            white = a
        elif o in ("-b", "--black"):
            black = a
        elif o in ("-r", "--result"):
            result = a
        elif o == "--elo_min":
            elo_min = int(a)
        elif o == "--elo_max":
            elo_max = int(a)
        else:
            assert False, "unhandled option"

    kwargs = {
        'player': player,
        'white': white,
        'black': black,
        'result': result,
        'elo_min': elo_min,
        'elo_max': elo_max
    }

    status = check_mandatory(options, opts)
    if status > 0:
        return status

    games = []

    pgn = pgn_load(file)
    game = chess.pgn.read_game(pgn)

    while game is not None:
        games.append(game)
        game = chess.pgn.read_game(pgn)

    filtered_games = search_pgn(games=games, **kwargs)

    for game in filtered_games:
        print(f'{game}\n')

    return status


if __name__ == '__main__':
    exit(main())
