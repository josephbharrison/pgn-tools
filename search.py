import sys
import getopt
import chess.pgn
from datetime import date
from common import pgn_load, print_usage, get_options, get_short_opts, get_long_opts, check_mandatory


def search_pgn(
        games: list = None,
        player: str = None,
        white: str = None,
        black: str = None,
        result: str = None,
        eco: str = None,
        opening: str = None,
        variation: str = None,
        event: str = None,
        site: str = None,
        game_date: str = None,
        event_date: str = None,
        date_min: str = None,
        date_max: str = None,
        elo_min: int = None,
        elo_max: int = None):

    _games = []

    for game in games:

        if game is None:
            continue

        if not game.headers:
            continue

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

        if eco:
            if eco.lower() != str(h['ECO']).lower():
                continue

        if opening:
            if result != h['Result']:
                continue

        if eco:
            if eco.lower() != str(h['ECO']).lower():
                continue

        if opening:
            if opening.lower() not in str(h['Opening']).lower():
                continue

        if variation:
            if variation.lower() not in str(h['Variation']).lower():
                continue

        if event:
            if event.lower() not in str(h['Event']).lower():
                continue

        if site:
            if site.lower() not in str(h['Site']).lower():
                continue

        if game_date:
            if 'Date' not in h:
                continue

            if game_date != h['Date']:
                continue

        if event_date:
            if 'EventDate' not in h:
                continue

            if event_date != h['EventDate']:
                continue

        if date_min or date_max:
            if 'EventDate' not in h and 'Date' not in h:
                continue

            if 'Date' in h:
                game_date = h['Date']
            else:
                game_date = h['EventDate']

            if date_min:
                date_str = date_min
            else:
                date_str = date_max

            game_year = int(game_date.split('.')[0])
            game_month = int(game_date.split('.')[1])
            game_day = int(game_date.split('.')[2])
            game_date = (game_year, game_month, game_day)

            search_year = int(date_str.split('.')[0])
            search_month = int(date_str.split('.')[1])
            search_day = int(date_str.split('.')[2])
            search_date = (search_year, search_month, search_day)

            if date_min:
                if search_date > game_date:
                    continue

            if date_max:
                if search_date < game_date:
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

    file = None
    kwargs = {
        'player': None,
        'white': None,
        'black': None,
        'result': None,
        'eco': None,
        'opening': None,
        'variation': None,
        'event': None,
        'site': None,
        'game_date': None,
        'event_date': None,
        'date_min': None,
        'date_max': None,
        'elo_min': None,
        'elo_max': None
    }

    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage('search', options)
            exit(0)
        elif o in ("-f", "--file"):
            file = a
        elif o in ("-p", "--player"):
            kwargs['player'] = a
        elif o in ("-w", "--white"):
            kwargs['white'] = a
        elif o in ("-b", "--black"):
            kwargs['black'] = a
        elif o in ("-r", "--result"):
            kwargs['result'] = a
        elif o in ("-e", "--eco"):
            kwargs['eco'] = a
        elif o in ("-o", "--opening"):
            kwargs['opening'] = a
        elif o in ("-V", "--variation"):
            kwargs['variation'] = a
        elif o in ("-E", "--event"):
            kwargs['event'] = a
        elif o in ("-s", "--site"):
            kwargs['site'] = a
        elif o in ("-d", "--game_date"):
            kwargs['game_date'] = a
        elif o in ("-D", "--event_date"):
            kwargs['event_date'] = a
        elif o == "--date_min":
            kwargs['date_min'] = a
        elif o == "--date_max":
            kwargs['date_max'] = a
        elif o == "--elo_min":
            kwargs['elo_min'] = int(a)
        elif o == "--elo_max":
            kwargs['elo_max'] = int(a)
        else:
            assert False, "unhandled option"

    status = check_mandatory(options, opts)
    if status > 0:
        return status

    games = []

    pgn = pgn_load(file)
    game = chess.pgn.read_game(pgn)

    while game is not None:
        games.append(game)
        try:
            game = chess.pgn.read_game(pgn)
        except ValueError as e:
            print(e)

    filtered_games = search_pgn(games=games, **kwargs)

    for game in filtered_games:
        print(f'{game}\n')

    return status


if __name__ == '__main__':
    exit(main())
