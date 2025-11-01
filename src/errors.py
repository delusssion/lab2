from pathlib import Path


def validate_path_exists(path):
    if not Path(path).exists():
        raise FileNotFoundError(f"'{path}' не существует")


def validate_is_file(path):
    if not Path(path).is_file():
        raise IsADirectoryError(f"'{path}' не является файлом")


def validate_is_directory(path):
    if not Path(path).is_dir():
        raise NotADirectoryError(f"'{path}' не является директорией")


def validate_not_self_copy(src, dst):
    if Path(dst).resolve().is_relative_to(Path(src).resolve()):
        raise ValueError('Нельзя копировать директорию в саму себя')
