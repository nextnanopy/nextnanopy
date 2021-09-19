import sys, os
import subprocess
import queue
import threading
from nextnanopy.utils.misc import get_filename, mkdir_if_not_exist
from nextnanopy import defaults


def command(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        **opt_kwargs,
):
    kwargs = dict(
        inputfile=inputfile,
        exe=exe,
        license=license,
        database=database,
        outputdirectory=outputdirectory,
    )
    kwargs.update(opt_kwargs)
    product = defaults.input_file_type(inputfile)
    cmd = defaults.get_command(product)
    return cmd(**kwargs)


def send(cmd):
    PIPE = subprocess.PIPE
    return subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True)


def read_output(pipe, funcs):
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line)
    pipe.close()


def write_output(get, filepath, show=True):
    f = open(filepath, 'w', newline='')
    for line in iter(get, None):
        line = str(line, 'utf-8', errors='ignore')
        if show:
            sys.stdout.write(line)
        f.write(line)
    f.close()


def start_log(process, filepath, show=True):
    q = queue.Queue()
    out, err = [], []
    tout = threading.Thread(
        target=read_output, args=(process.stdout, [q.put, out.append]))
    terr = threading.Thread(
        target=read_output, args=(process.stderr, [q.put, err.append]))
    twrite = threading.Thread(target=write_output, args=(q.get, filepath, show))
    for t in (tout, terr, twrite):
        t.daemon = False
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
        show_log=True,
        **kwargs,
):
    filename = get_filename(inputfile, ext=False)
    inputfile = os.path.abspath(inputfile)
    outputdirectory = os.path.join(outputdirectory, filename)
    mkdir_if_not_exist(outputdirectory)
    logfile = os.path.join(outputdirectory, f'{filename}.log')
    cmd = command(inputfile, exe, license, database, outputdirectory, **kwargs)
    cwd = os.getcwd()
    wdir = os.path.split(exe)[0]  # nn3 assumes wdir at one folder upper than the executable
    os.chdir(wdir)
    process = send(cmd)
    start_log(process, logfile, show_log)
    os.chdir(cwd)
    info = {
        'process': process,
        'outputdirectory': outputdirectory,
        'filename': filename,
        'logfile': logfile,
        'cmd': cmd,
        'wdir': wdir,
    }
    return info
