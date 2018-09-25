import os
import ast


def _get_cl_args():
    dict_string = '{}'
    data_dict = {}

    try:
        dict_string = os.environ['DICT_STRING']
    except KeyError:
        pass

    try:
        data_dict = ast.literal_eval(dict_string)
    except ValueError:
        pass
    except SyntaxError:
        pass

    return data_dict


def get_value(dict_key, default_value=None):
    data_dict = _get_cl_args()

    return data_dict.get(dict_key, default_value)
