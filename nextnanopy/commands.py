import sys, os
import subprocess
import queue
import threading
from .utils.misc import get_filename, mkdir_if_not_exist
from .utils.formatting import is_nn3_input_file, is_nnp_input_file
from collections import OrderedDict


def _path(path):
    if path:
        path = r'{}'.format(path)
        path = f'"{path}"'
    return path


def _bool(_in):
    if _in == 0:
        return True
    else:
        return bool(_in)


def command(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        **kwargs,
):
    cmd_kwargs = dict(
        inputfile=inputfile,
        exe=exe,
        license=license,
        database=database,
        outputdirectory=outputdirectory,
    )
    cmd_kwargs.update(kwargs)
    if is_nn3_input_file(inputfile):
        return command_nn3(**cmd_kwargs)
    elif is_nnp_input_file(inputfile):
        return command_nnp(**cmd_kwargs)
    else:
        raise ValueError(f'Input file is not valid')


def generate_command(args):
    cmd = []
    for case in args:
        arg, value = case
        _a, _v = _bool(arg), _bool(value)
        if not _a:
            continue
        elif _a and not _v:
            cmdi = f"{arg}"
        else:
            cmdi = f"{arg} {value}"
        cmd.append(cmdi)
    cmd = ' '.join(cmd)
    return cmd


def command_nn3(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        threads=0,
        debuglevel=0,
        cancel=-1,
        softkill=-1,
        **kwargs,
):
    cmd_args = OrderedDict(
        exe=[_path(exe), ''],
        license=['-license', _path(license)],
        inputfile=['-inputfile', _path(inputfile)],
        database=['-database', _path(database)],
        threads=['-threads', threads],
        outputdirectory=['-outputdirectory', _path(outputdirectory)],
        debuglevel=['-debuglevel', debuglevel],
        cancel=['-cancel', cancel],
        softkill=['-softkill', softkill],
    )
    return generate_command(cmd_args.values())


def command_nnp(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        threads=0,
        **kwargs,
):
    cmd_args = OrderedDict(
        exe=[_path(exe), ''],
        license=['--license', _path(license)],
        database=['--database', _path(database)],
        threads=['--threads', threads],
        outputdirectory=['--outputdirectory', _path(outputdirectory)],
        noautooutdir=['--noautooutdir', ''],
        inputfile=[_path(inputfile), ''],
    )
    return generate_command(cmd_args.values())


def send(cmd):
    PIPE = subprocess.PIPE
    return subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True)


def read_output(pipe, funcs):
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line)
    pipe.close()


def write_output(get, filepath):
    f = open(filepath, 'w', newline='')
    for line in iter(get, None):
        line = str(line, 'utf-8', errors='ignore')
        sys.stdout.write(line)
        f.write(line)
    f.close()


def start_log(process, filepath):
    q = queue.Queue()
    out, err = [], []
    tout = threading.Thread(
        target=read_output, args=(process.stdout, [q.put, out.append]))
    terr = threading.Thread(
        target=read_output, args=(process.stderr, [q.put, err.append]))
    twrite = threading.Thread(target=write_output, args=(q.get, filepath))
    for t in (tout, terr, twrite):
        t.daemon = True
        t.start()
    process.wait()
    for t in (tout, terr):
        t.join()
    q.put(None)


def execute(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        **kwargs,
):
    filename = get_filename(inputfile, ext=False)
    outputdirectory = os.path.join(outputdirectory, filename)
    mkdir_if_not_exist(outputdirectory)
    logfile = os.path.join(outputdirectory, f'{filename}.log')
    cmd = command(inputfile, exe, license, database, outputdirectory, **kwargs)
    cwd = os.getcwd()
    wdir = os.path.split(exe)[0] # nn3 assumes wdir at one folder upper than the executable
    print(wdir)
    os.chdir(wdir)
    process = send(cmd)
    start_log(process, logfile)
    os.chdir(cwd)
    return process
