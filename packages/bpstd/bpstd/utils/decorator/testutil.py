# -*- coding: utf-8 -*-

import time


def func_performance(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        for x in range(5000):
            results = func(*args, **kwargs)
        t2 = time.time()
        print('took  {}ms' .format((t2 - t1) * 1000))
        return results
    return wrapper
