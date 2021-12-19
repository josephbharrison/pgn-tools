import sys
import getopt
import chess.pgn
from datetime import date
from common import pgn_load, print_usage, get_options, get_short_opts, get_long_opts, check_mandatory


def search_pgn(
        games: list = None,
        player: str = None,
        team: str = None,
        white_team: str = None,
        black_team: str = None,
        fide_id: str = None,
        white_fide_id: str = None,
        black_fide_id: str = None,
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
            if player.lower() not in str(h['White']).lower() and player not in str(h['Black']).lower():
                continue

        if white:
            if white.lower() not in str(h['White']).lower():
                continue

        if black:
            if black.lower() not in str(h['Black']).lower():
                continue

        if team:
            if 'WhiteTeam' not in h:
                h['WhiteTeam'] = ''

            if 'BlackTeam' not in h:
                h['BlackTeam'] = ''

            if team.lower() not in str(h['WhiteTeam']).lower() and team.lower() not in str(h['BlackTeam']).lower():
                continue

        if white_team:
            if 'WhiteTeam' not in h:
                continue

            if white_team.lower() not in str(h['WhiteTeam']).lower():
                continue

        if black_team:
            if 'BlackTeam' not in h:
                continue

            if black_team.lower() not in str(h['BlackTeam']).lower():
                continue

        if fide_id:
            if 'WhiteFideId' not in h:
                h['WhiteFideId'] = ''

            if 'BlackFideId' not in h:
                h['BlackFideId'] = ''

            if fide_id not in h['WhiteFideId'] and fide_id not in h['BlackFideId']:
                continue

        if white_fide_id:
            if 'WhiteFideId' not in h:
                continue

            if white_fide_id != h['WhiteFideId']:
                continue

        if black_fide_id:
            if 'BlackFideId' not in h:
                continue

            if white_fide_id != h['BlackFideId']:
                continue

        if result:
            if 'Result' not in h:
                continue

            if result != h['Result']:
                continue

        if eco:
            if 'ECO' not in h:
                continue

            if eco.lower() != str(h['ECO']).lower():
                continue

        if opening:
            if 'Opening' not in h:
                continue

            if result != h['Result']:
                continue

        if variation:
            if 'Variation' not in h:
                continue

            if variation.lower() not in str(h['Variation']).lower():
                continue

        if event:
            if 'Event' not in h:
                continue

            if event.lower() not in str(h['Event']).lower():
                continue

        if site:
            if 'Site' not in h:
                continue

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
            game_date = date(game_year, game_month, game_day)

            search_year = int(date_str.split('.')[0])
            search_month = int(date_str.split('.')[1])
            search_day = int(date_str.split('.')[2])
            search_date = date(search_year, search_month, search_day)

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
        'team': None,
        'white_team': None,
        'black_team': None,
        'fide_id': None,
        'white_fide_id': None,
        'black_fide_id': None,
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
        elif o in ("-t", "--team"):
            kwargs['team'] = a
        elif o == "--white_team":
            kwargs['white_team'] = a
        elif o == "--black_team":
            kwargs['black_team'] = a
        elif o in ("-F", "--fide_id"):
            kwargs['fide_id'] = a
        elif o == "--white_fide_id":
            kwargs['white_fide_id'] = a
        elif o == "--black_fide_id":
            kwargs['black_fide_id'] = a
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
