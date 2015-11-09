import functools

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("%s called with %s, %s" % (
            func.__name__,
            [str(arg) for arg in args],
            kwargs,
            ))
        results = func(*args, **kwargs)
        print("\t--->%s" %  results)
        return results
    return wrapper
