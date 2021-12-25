import yaml

CONFIGPATH = 'config'


# Conversion functions
def format_annotations(a: list):
    return {ant[0]: ant[1] for ant in a}


def format_game(g: list):
    return {
        'moves': g[0],
        'outcome': g[1]
    }


def format_entry(e: list):
    return {'annotations': e[0], 'game': e[1]}


def handle_optional(m):
    if len(m) > 0:
        return m[0]
    else:
        return None


def pgn_load(pgn_file: str):
    pgn = open(pgn_file)
    return pgn


def get_config(file, config_path: str = None) -> dict:
    config = {}

    if config_path is None:
        config_path = CONFIGPATH

    with open(f'{config_path}/{file}', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'invalid configuration: config/{file}')
            print(exc)
            exit(1)

    return config


def get_short_opts(options: dict = None) -> str:

    short_opts = ''
    for opt, value in options.items():
        if 'short' in value.keys():
            if value['arg']:
                short_opts += f'{value["short"]}:'
            else:
                short_opts += f'{value["short"]}'

    return short_opts


def check_mandatory(options: dict = None, opts: list = None) -> int:
    status = 0
    missing_mandatory = False
    mandatory_opts = []
    for k, v in options.items():
        if 'mandatory' in v.keys() and v.get('mandatory') is True:
            missing_mandatory = True
            mandatory_opts = [f'--{k}']
            if 'short' in v.keys():
                mandatory_opts.append(f'-{v.get("short")}')
            for o, a in opts:
                if o in mandatory_opts:
                    missing_mandatory = False
                    break
        if missing_mandatory:
            break
    if missing_mandatory:
        status = 2
        print(f'missing mandatory option: {mandatory_opts}')
    return status


def get_long_opts(options: dict = None) -> list:

    long_opts = []
    for opt, value in options.items():
        if value['arg']:
            long_opts.append(f'{opt}=')
        else:
            long_opts.append(f'{opt}')

    return long_opts


def get_options(option_type: str):
    options = get_config('options.yaml')[option_type]
    return options


def print_usage(name: str = None, options: dict = None):

    def buffer_opt(opt_str: str, max_len: int = 0):
        while len(opt_str) < max_len:
            opt_str += ' '
        return opt_str

    print(f'{name} usage:')
    opt_width = 0
    for k, v in options.items():
        o = ''
        if 'short' in v.keys():
            o = f'    -{v["short"]}, '
            o += f'--{k}'
        else:
            o += f'    --{k}'
        if 'type' in v.keys():
            o += f' <{v["type"]}>'
        o += '  '
        options[k].update({'opt_str': o})
        if len(o) > opt_width:
            opt_width = len(o)

    for k, v in options.items():
        opt = buffer_opt(v['opt_str'], opt_width)
        desc = v["desc"]
        args = ''
        if 'args' in v:
            for arg in v['args']:
                args += f' {arg},'
            args = args.rstrip(',').lstrip(' ')

        if args:
            print(f'{opt} {desc}: ({args})')
        else:
            print(f'{opt} {desc}')
    print()