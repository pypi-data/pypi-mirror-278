import os
import re
import time
from typing import Union

pattern = re.compile(r'\$\{([^{}]+?)\}')


def get_now_str(format='%Y%m%d%H%M%S') -> str:
    return time.strftime(format)


def isTrue(value):
    false_values = {'false', 'no', '0', 'n', 'f', ''}
    true_values = {'true', 'yes', '1', 'y', 't'}

    if isinstance(value, bool):
        return value

    if value is None:
        return False

    if isinstance(value, str):
        str_value = str(value).strip().lower()

        if str_value in false_values:
            return False
        elif str_value in true_values:
            return True

    return value


def seconds2hms(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return int(hours), int(minutes), int(seconds)


def replace_env_variables(text: str) -> str:
    matches = re.finditer(pattern, text)
    match = matches.__next__()
    value = retrieve_environment(match.group(1))
    if match.regs[0][0] == 0 and match.regs[0][1] == len(text):
        return value
    else:
        text = text.replace(match.group(0), str(value))
    for match in matches:
        value = retrieve_environment(match.group(1))
        text = text.replace(match.group(0), str(value))
    return text


def retrieve_environment(env_k: str) -> Union[str, int, float]:
    env_reType_dict = {
        'int': int,
        'float': float,
        'str': str
    }

    v_default, v_type = None, None
    if '|' in env_k:
        key_item = env_k.split('|')
        for info in key_item[1:]:
            if info.startswith('default:'):
                v_default = info.strip().replace('default:', '')
            if info.startswith('type:'):
                v_type = info.strip().replace('type:', '')
        env_k = key_item[0]
    v = os.getenv(env_k, v_default)
    if v_type in env_reType_dict:
        v = env_reType_dict[v_type](v)
    return v
