import _ctypes
import json
from collections import UserList, defaultdict
from pathlib import Path

import pandas as pd

from .utils import _path_suffix_check, _save_string_to_file


def di(obj_id):
    """Inverse of id() function."""
    return _ctypes.PyObj_FromPtr(obj_id)


class Records(list[dict]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_list(self) -> list:
        return list(self)

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            list(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            _save_string_to_file(ret, path)
        return ret

    def from_json(self, path: str | Path):
        with open(path, encoding="utf-8") as file:
            super().extend(json.load(file))
        return self

    def to_dict(self, keys: list) -> defaultdict:
        ret: defaultdict = defaultdict(dict)
        for record in self:
            p = id(ret)
            key_values = [record[key] for key in keys]
            key_values_len = len(key_values)
            for i in range(key_values_len):
                if i < key_values_len - 1:
                    # if di(p)[key_values[i]] exists
                    if key_values[i] not in di(p):
                        di(p)[key_values[i]] = {}
                    p = id(di(p)[key_values[i]])
                else:
                    if key_values[i] in di(p):
                        raise ValueError("Keys should be unique in the dataset.")
                    di(p)[key_values[i]] = record

        return ret
