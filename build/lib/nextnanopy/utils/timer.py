import time


def timer(method, fmt=lambda name, t: f'[Timer] {name}: {t * 1000:2.2f} ms', apply=True):
    if not apply:
        return method

    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        stop = time.time()
        elapse = (stop - start)
        print(fmt(method.__name__, elapse))
        return result

    return timed
