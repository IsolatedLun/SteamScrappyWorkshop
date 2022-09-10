import os
from shlex import split as shlex_split

from src.consts import BASE_DIR, DASH_LENGTH, OUTPUT_IDENTIFIER, BLACKLISTED_DIRS, STEAMCMD_LOGIN, CONFIG
from src.handlers.alias_handler import get_alias_by_app_id
from src.utils import clean_newlines, clean_quotes, count_sub_str, create_random_char, get_arg_index, sub_str

def convert_txt_to_scrappyd(path: str):
        temp = path.rsplit('.', maxsplit=1)[0] # Removes the file's extension
        temp += f'.{OUTPUT_IDENTIFIER}'

        return temp

# {'app_id': app_id, 'name': name, 'id': id}
def create_scrappyd_file(path: str, data: dict):
    """
        Creates a scrappyd file that has all the relevant info of it's text file counterpart

        FILE SPEC:
        MOD_COUNT
        ...
        MOD_NAME MOD_APP_ID MOD_ID
        ...
    """

    path = convert_txt_to_scrappyd(path)
    with open(path, 'w') as f:
        f.write(str(len(data)) + '\n')

        for item in data.keys():
            (app_id, name, _id, *_) = data[item].values()
            mod = f'"{clean_quotes(name)}"' + ' ' + app_id + ' ' + _id + '\n'
            f.write(mod)

def parse_scrappyd_file(text_path: str):
    data = {'items': {}, 'count': 0}
    
    path = convert_txt_to_scrappyd(text_path)
    with open(path, 'r') as f:
        f.seek(0)

        data['count'] = f.readline()
        for line in f.readlines():
            name, app_id, _id, *_ = shlex_split(line)
            data['items'][name] = {'app_id': app_id, 'id': _id}

    return data, data['count']

def create_output_file(out: str, data: dict, options: list[str], *vars: list[str]):
    """
        Creates an output text file that contains the command to donwload the items with steamcmd
    """
    def fix_out_dir(out_dir: str):
        """
            Appends the [scrappyd] identifier at the end of the text file's name 
        """
        temp = out_dir

        if out_dir.endswith('.txt'):
            temp = out_dir[0:len(out_dir) - 4]
        
        if not sub_str(out_dir, f'[{OUTPUT_IDENTIFIER}]'):
            temp += f'[{OUTPUT_IDENTIFIER}]'
        temp += '.txt'

        return temp

    def generate_file_name(vars: list[str]):
        return '-'.join(vars) + f'-{create_random_char(3)}'

    out_dir = ''
    has_multiple_params = False

    if '--dir' in options:
        idx = get_arg_index(options, '--dir')

        if not len(options) > idx + 1:
            out_dir = clean_quotes(options[idx])
        else:
            has_multiple_params = True

    # If the user hasn't specified the output in the cli and there is an out_dir in the config
    if not out_dir and CONFIG['out_dir'] and has_multiple_params:
        options.remove('--dir') # This is removed since it's useless

        if len(options) > count_sub_str(CONFIG['out_dir'], '{}'):
            raise Exception('Too many parameters for output directory')

        fname = ''
        if len(options) == 0:
            fname = generate_file_name(vars)
        else:
            fname = generate_file_name(vars) if options[-1] == '*'  else generate_file_name(options[-1])
            try:
                options.remove('*') # This is removed to avoid invalid argument errors
            except:
                pass

        out_dir = CONFIG['out_dir'].format(*options, fname)
    elif not out_dir and CONFIG['out_dir']:
        root_dir = CONFIG['out_dir'].split('/')[0]
        out_dir = os.path.join(root_dir, generate_file_name(vars))
    elif not out_dir:
        out_dir = generate_file_name(vars)

    # After creating the out_dir, we append the [scrappyd] string to the file name, so that we can access it later
    # This makes sure that the program only interacts with files that have [scrappyd] in their names
    # Preventing accidential overrides/deletions of other non-related files
    out_dir = fix_out_dir(os.path.join(BASE_DIR, out_dir))

    os.makedirs(os.path.dirname(out_dir), exist_ok=True)
    with open(out_dir, CONFIG['mode']) as f:
        f.seek(0)  # goto the 1st line

        file_data = f.readline()

        if file_data.startswith('steamcmd'):
            f.write(out)
        else:
            f.write(STEAMCMD_LOGIN + out)

    create_scrappyd_file(out_dir, data)
    return out_dir

def remove_text_and_scrappyd_files_by_index(idx: int):
    file = get_scrappyd_file_by_index(idx)

    if file:
        os.remove(file)
        os.remove(convert_txt_to_scrappyd(file))

        return file
    else:
        raise Exception(f'> The file with an index of "{idx}" does not exist')

def get_scrappyd_files():
    """
        Searches every directory and files beginning from the current dir,
        and adds an file if it's ends with [scrappyd]
    """
    files_dict = {}
    for root, dirs, files in os.walk(BASE_DIR, topdown=True):
        if dirs in BLACKLISTED_DIRS:
            break

        for file in files:
            if sub_str(file, f'[{OUTPUT_IDENTIFIER}].txt'):
                files_dict[file] = f'{root}/{file}'

    return files_dict

def get_scrappyd_file_by_index(idx: int):
    files = get_scrappyd_files()

    if idx > len(files) - 1:
        raise Exception(f'> The file with an index of "{idx}" does not exist') 

    for i, (name, path) in enumerate(files.items()):
        if i == idx:
            return path
    return None


# =========================
# Misc functions
# =========================
def show_files():
    files = get_scrappyd_files()

    print('\n' + '-' * DASH_LENGTH)
    for i, (name, path) in enumerate(files.items()):
        print(f'| {name} -> [{i}]')
        print('-' * DASH_LENGTH)

def show_file(idx: int):
    file = get_scrappyd_file_by_index(idx)
    data, count = parse_scrappyd_file(file)

    print('\n' + '-' * DASH_LENGTH)
    for (name, values) in data['items'].items():
        alias = get_alias_by_app_id(values['app_id'])

        print(f'| {clean_quotes(name)} -> {values["id"]} [{alias}]')
        print('-' * DASH_LENGTH)
    
    return clean_newlines(count)