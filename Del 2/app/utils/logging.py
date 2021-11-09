from time import time

def time_function_log(func, *args, **kwargs):
    start = time()
    return_value = func(*args, **kwargs)
    end = time()
    with open("latest.log", "a") as file:
        file.write("{} took {:.4f} seconds to execute.\n".format(func.__name__, end - start))

    return return_value