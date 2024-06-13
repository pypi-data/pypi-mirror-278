from pathlib import Path


def _save_string_to_file(string: str, path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(string)

    return


def _path_suffix_check(path: Path | str, suffix: str) -> Path:
    if isinstance(path, str):
        path = Path(path)

    if path.suffix != suffix:
        path = path.with_suffix(suffix)
    return path
