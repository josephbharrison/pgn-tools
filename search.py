import sys
import getopt
import chess.pgn
from datetime import date
from common import pgn_load, print_usage, get_options, get_short_opts, get_long_opts, check_mandatory


def search_pgn(
        headers,
        offset,
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

    r = None

    while True:
        # players
        pgn_white = headers.get('White', '?')
        pgn_black = headers.get('Black', '?')

        if player:
            if player.lower() not in pgn_white.lower() and player not in pgn_black.lower():
                break

        if white:
            if white.lower() not in pgn_white.lower():
                break

        if black:
            if black.lower() not in pgn_black.lower():
                break

        pgn_white_team = headers.get('WhiteTeam', '?')
        pgn_black_team = headers.get('BlackTeam', '?')

        # team
        if team:
            if team.lower() not in pgn_white_team.lower() and team.lower() not in pgn_black_team.lower():
                break

        if white_team:
            if white_team.lower() not in pgn_white_team.lower():
                break

        if black_team:
            if black_team.lower() not in pgn_black_team.lower():
                break

        pgn_white_fide_id = headers.get('WhiteFideId', '?')
        pgn_black_fide_id = headers.get('BlackFideId', '?')

        # fide_id
        if fide_id:
            if fide_id not in pgn_white_fide_id and fide_id not in pgn_black_fide_id:
                break

        if white_fide_id:
            if white_fide_id != pgn_white_fide_id:
                break

        if black_fide_id:
            if black_fide_id != pgn_black_fide_id:
                break

        # result
        pgn_result = headers.get('Result', '?')
        if result:
            if result != pgn_result:
                break

        # eco
        pgn_eco = headers.get('ECO', '?')
        if eco:
            if eco.lower() != pgn_eco.lower():
                break

        # opening
        pgn_opening = headers.get('Opening', '?')
        if opening:
            if opening.lower() not in pgn_opening.lower():
                break

        # variation
        pgn_variation = headers.get('Variation', '?')
        if variation:
            if variation.lower() not in pgn_variation.lower():
                break

        # event
        pgn_event = headers.get('Event', '?')
        if event:
            if event.lower() not in pgn_event.lower():
                break

        # site
        pgn_site = headers.get('Site', '?')
        if site:
            if site.lower() not in pgn_site.lower():
                break

        # game_date
        pgn_date = headers.get('Date', '?')
        if game_date:
            if game_date != pgn_date:
                break

        # event_date
        pgn_event_date = headers.get('EventDate', '?')
        if event_date:
            if event_date != pgn_event_date:
                break

        if date_min or date_max:
            if pgn_date == '?' and pgn_event_date == '?':
                break

            if pgn_date != '?':
                game_date = pgn_date
            else:
                game_date = pgn_event_date

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
                    break

            if date_max:
                if search_date < game_date:
                    break

        # elo_min
        pgn_white_elo = headers.get('WhiteElo', '?')
        pgn_black_elo = headers.get('BlackElo', '?')

        if elo_min:
            if pgn_white_elo == '?' or pgn_black_elo == '?':
                break

            if elo_min > int(pgn_white_elo):
                offset = None

            if elo_min > int(pgn_black_elo):
                offset = None

        if elo_max:
            if pgn_white_elo == '?' or pgn_black_elo == '?':
                break

            if elo_max < int(pgn_white_elo):
                offset = None

            if elo_max < int(pgn_black_elo):
                offset = None

        r = offset
        break

    return r


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
    offsets = []

    while True:
        offset = pgn.tell()
        headers = chess.pgn.read_headers(pgn)
        if headers is None:
            break
        filtered_offset = search_pgn(headers=headers, offset=offset, **kwargs)
        if filtered_offset:
            offsets.append(filtered_offset)

    for offset in offsets:
        pgn.seek(offset)
        games.append(chess.pgn.read_game(pgn))

    for game in games:
        print(f'{game}\n')

    return status


if __name__ == '__main__':
    exit(main())
