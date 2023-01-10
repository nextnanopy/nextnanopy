import os
import numpy as np

def is_file(fullpath):
    filename = os.path.split(fullpath)[-1]
    if '.' not in filename:
        bool = False
    else:
        bool = True
    return bool


def get_filename(fullpath, ext=True):
    if not is_file(fullpath):
        raise ValueError(f'{fullpath} is not a file')
    filename = os.path.split(fullpath)[-1]
    if not ext:
        filename = os.path.splitext(filename)[0]
    return filename


def get_file_extension(fullpath):
    if not is_file(fullpath):
        raise ValueError(f'{fullpath} is not a file')
    filename = os.path.split(fullpath)[-1]
    ext = f".{filename.split('.')[-1]}"
    return ext


def get_folder(fullpath):
    if not is_file(fullpath):
        folder = fullpath
    else:
        folder = os.path.split(fullpath)[0]
    return folder


def get_path_files(path):
    if path == '':
        path = '.'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files


def mkdir_if_not_exist(path):
    from pathlib import Path
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def find_unused_name(name, list_names, extension, max_idx=True):
    if extension[0] != '.':
        extension = f'.{extension}'
    if extension not in name:
        name += extension
    prefix = get_file_prefix(name)
    lnames = list(filter(lambda ln: extension in ln and prefix in ln, list_names))

    if len(lnames) == 0:
        max_idx = 0
    if max_idx:
        idxs = [get_file_idx(name) for name in lnames]
        idxs.sort()
        max_idx = idxs[-1]
        unused_name = f'{prefix}_{max_idx + 1}{extension}'
    else:
        idx = 0
        unused_name = f'{prefix}_{idx}{extension}'
        while unused_name in list_names:
            unused_name = f'{prefix}_{idx}{extension}'
            idx += 1
    return unused_name


def find_unused_in_folder(fullpath, overwrite=False):
    #folder, name = os.path.split(fullpath)
    name = os.path.basename(fullpath)
    folder = os.path.dirname(fullpath)
    ext = get_file_extension(name)
    cwd_files = get_path_files(folder)
    if not overwrite:
        name = find_unused_name(name, cwd_files, ext)
    return os.path.join(folder, name)


def savetxt(fullpath, text, overwrite=False, automkdir=True):
    if automkdir:
        mkdir_if_not_exist(get_folder(fullpath))
    fullpath = find_unused_in_folder(fullpath, overwrite)
    with open(fullpath, 'w+') as file:
        file.write(text)
    return fullpath


def get_file_prefix(file):
    prefix, ext = os.path.splitext(file)
    idx = get_file_idx(prefix)
    if idx > -1:
        prefix = '_'.join(prefix.split('_')[0:-1])
    return prefix


def get_file_idx(file):
    prefix, ext = os.path.splitext(file)
    idx = -1
    if '_' in prefix:
        end = prefix.split('_')[-1]
        try:
            idx = int(end)
        except:
            pass
    return idx


def message_decorator(method, init_msg=None, end_msg=None):
    def f(*args, **kwargs):
        show_message(init_msg)
        result = method(*args, **kwargs)
        show_message(end_msg)
        return result

    return f


def show_message(msg):
    if msg is None:
        return
    if type(msg) == str:
        print(msg)
    elif callable(msg):
        msg()
    else:
        pass

def mkdir_even_if_exists(path,name):
    """creates a directory under path with a given name. If exists, adds integer number to directory name.
    returns directory full path"""
    directory = os.path.join(path,name)
    if os.path.exists(directory):
        i = 0
        while True:
            directory_numbered = directory +str(i)
            if os.path.exists(directory_numbered):
                i+=1
            elif i>2147483646:
                raise StopIteration('too many folders with the same name')
            else:
                os.makedirs(directory_numbered)
                directory = directory_numbered
                break
    else:
        os.makedirs(directory)
    return directory


def combinations(*args):
    n = len(args)
    array_of_combinations = np.array(np.meshgrid(*args)).T.reshape(-1,n)
    return array_of_combinations

def start_with_choice(line : str, *args : str):
    for arg in args:
        if line.startswith(args):
            return True
    return False