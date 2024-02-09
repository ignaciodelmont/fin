from functools import wraps


def map_res_with_type(st_type, res):
    if not res:
        return res

    needed_keys = list(st_type.__init__.__code__.co_varnames)[1:]
    base = st_type(**{k: res.get(k) for k in needed_keys})
    base.__setattr__("db_raw_data", res)
    return base


def convert_result(st_type):
    @wraps
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if type(res) == list:
                return [map_res_with_type(st_type, i) for i in res]
            return map_res_with_type(st_type, res)

        return inner_wrapper

    return wrapper
