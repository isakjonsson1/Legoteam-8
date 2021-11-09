"""Logging functions"""
from time import time


def time_function_log(func, *args, **kwargs):
    """Used to time a function"""
    start = time()
    return_value = func(*args, **kwargs)
    end = time()
    with open("latest.log", "a", encoding="utf-8") as file:
        file.write(
            "{} took {:.4f} seconds to execute.\n".format(func.__name__, end - start)
        )

    return return_value
