import inspect
from datetime import datetime
from typing import Any, Literal, Union, get_args, get_origin

from typing_extensions import Literal as LiteralEx

try:
    import pandas as pd
except ImportError:
    pd = None

from dvcx.sql.types import (
    JSON,
    Array,
    Binary,
    Boolean,
    DateTime,
    Float,
    Int,
    NullType,
    SQLType,
    String,
)

TYPE_FROM_DVCX = {
    Int: int,
    String: str,
    Float: float,
    Boolean: bool,
}


TYPE_TO_DVCX = {
    int: Int,
    str: String,
    Literal: String,
    LiteralEx: String,
    float: Float,
    bool: Boolean,
    datetime: DateTime,
    bytes: Binary,
    list: Array(NullType),
    dict: JSON,
    Any: NullType,
    None: NullType,
}


class DvcxError(Exception):
    def __init__(self, message):
        super().__init__(message)


def row_to_pandas(args, params):
    data = dict(zip([i.name for i in params], args))
    return pd.Series(data, name=data.get("name"))


def row_list_to_pandas(args, params):
    return pd.DataFrame(args, columns=[i.name for i in params])


def bin_to_array(data):
    return [
        int.from_bytes(data[i : i + 4], byteorder="big") for i in range(0, len(data), 4)
    ]


def array_to_bin(integers):
    return b"".join(int.to_bytes(i, length=4, byteorder="big") for i in integers)


def union_dicts(*dicts):
    """Union dictionaries.
    Equivalent to `d1 | d2 | d3` in Python3.9+ but works in older versions.
    """
    result = None
    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError("All arguments must be dictionaries.")
        if not result:
            result = d.copy()
        else:
            result.update(d)
    return result


def convert_type_to_dvcx(typ):  # noqa: PLR0911
    if inspect.isclass(typ) and issubclass(typ, SQLType):
        return typ
    res = TYPE_TO_DVCX.get(typ)
    if res:
        return res

    orig = get_origin(typ)

    if orig in (Literal, LiteralEx):
        return String

    args = get_args(typ)
    if inspect.isclass(orig) and (issubclass(list, orig) or issubclass(tuple, orig)):
        if args is None or len(args) != 1:
            raise TypeError(f"Cannot resolve type '{typ}' for flattening features")
        next_type = convert_type_to_dvcx(args[0])
        return Array(next_type)

    if inspect.isclass(orig) and issubclass(dict, orig):
        return JSON

    if orig == Union and len(args) == 2 and (type(None) in args):
        return convert_type_to_dvcx(args[0])

    # Special case for list in JSON: Union[dict, list[dict]]
    if orig == Union and len(args) >= 2:
        args_no_nones = [arg for arg in args if arg != type(None)]
        if len(args_no_nones) == 2:
            args_no_dicts = [arg for arg in args_no_nones if arg != dict]
            if len(args_no_dicts) == 1 and get_origin(args_no_dicts[0]) == list:
                arg = get_args(args_no_dicts[0])
                if len(arg) == 1 and arg[0] == dict:
                    return JSON

    raise TypeError(f"Cannot recognize type {typ}")
