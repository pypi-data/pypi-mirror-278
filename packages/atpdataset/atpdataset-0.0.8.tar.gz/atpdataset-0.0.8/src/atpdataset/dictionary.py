import json
from collections import defaultdict
from pathlib import Path

import toml
import yaml

from .utils import _path_suffix_check, _save_string_to_file


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            dict(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            _save_string_to_file(ret, path)
        return ret

    def to_yaml(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = yaml.dump(
            dict(self),
            default_flow_style=False,
            allow_unicode=True,
            indent=indent,
        )
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def to_toml(self, path: str | Path | None = None) -> str:
        ret = toml.dumps(dict(self))
        if path is not None:
            _save_string_to_file(ret, path)
        return ret


class DictDefault(defaultdict):
    def __init__(self, *args, **kwargs):
        super().__init__(dict, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict(self)

    def to_defaultdict(self) -> dict:
        return defaultdict(dict, self)

    def from_dict(self, dict_: defaultdict | dict):
        super().update(dict_)
        return self

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            dict(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            _save_string_to_file(ret, path)
        return ret

    def to_yaml(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = yaml.dump(
            dict(self),
            default_flow_style=False,
            allow_unicode=True,
            indent=indent,
        )
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def to_toml(self, path: str | Path | None = None) -> str:
        ret = toml.dumps(dict(self))
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def from_file(self, path: str | Path):
        if isinstance(path, str):
            path = Path(path)

        suffix = path.suffix
        match suffix:
            case ".json":
                self.from_json(path)
            case ".yaml" | ".yml":
                self.from_yaml(path)
            case ".toml":
                self.from_toml(path)
            case _:
                raise ValueError("Invalid file format")

        return self

    def from_json(self, path: str | Path):
        with open(path, encoding="utf-8") as file:
            super().update(json.load(file))
        return self

    def from_yaml(self, path: str | Path):
        with open(path, encoding="utf-8") as file:
            super().update(yaml.safe_load(file))
        return self

    def from_toml(self, path: str | Path):
        with open(path, encoding="utf-8") as file:
            super().update(toml.load(file))
        return self
