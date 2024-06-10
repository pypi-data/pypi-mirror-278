import logging
from typing import Optional, Union, Any, List
from uuid import UUID


def strcmp(s1: str, s2: str):
    if s1 < s2:
        return -1
    elif s1 > s2:
        return 1
    else:
        return 0


def str2bool(val: Union[str, bool, int]) -> bool:
    """
    Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return bool(val)
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def parse_device_list(device_list: Union[str, None]) -> Union[List[int], str]:
    if device_list is None:
        return 'auto'
    elif device_list == 'auto':
        return 'auto'
    elif device_list == 'cpu':
        return 'cpu'

    return [int(device) for device in device_list.split(',')]


def str_args_to_list(str_args: Union[str, List[str]]) -> List[str]:
    return str_args.split(',') if isinstance(str_args, str) else str_args


def uuid_from_any(value: Any) -> Optional[UUID]:
    if not value:
        return None
    if isinstance(value, UUID):
        return value
    else:
        try:
            return UUID(value)
        except ValueError:
            logging.exception(f"bad value {value}")


def str2loglevel(value: Union[str, int]) -> Optional[int]:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        level: Union[int, str] = logging.getLevelName(value)
        if isinstance(level, int):
            return level
    return None


def str2bool_from_dict(input_dict, key: str, default: bool) -> bool:
    default_str = "true" if default else "false"
    return str2bool(input_dict.get(key, default_str))


def merge_dicts(d1: dict, d2: dict, d3: Optional[dict] = None) -> dict:
    """
    Merge two or three dictionaries into d1 and return it
    """
    d1.update(d2)
    if d3:
        d1.update(d3)
    return d1


def concat_lists(l1: Optional[list], l2: Optional[list]) -> Optional[list]:
    """
    Concatenate two lists into a single list. Returns None if both lists are None.
    If only one list is provided, returns that list. If both are provided, returns their concatenation.
    """
    if l1 is None and l2 is None:
        return None
    elif l1 is None:
        return l2
    elif l2 is None:
        return l1
    else:
        return l1 + l2
