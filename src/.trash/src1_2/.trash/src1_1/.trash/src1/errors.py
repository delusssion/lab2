import shutil
from pathlib import Path


class CommandContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.handle_error(exc_type, exc_val)
            return True
        return False

    def handle_error(self, exc_type, exc_val):
        error_map = {
            PermissionError: 'Ошибка: Доступ запрещен',
            FileNotFoundError: 'Ошибка: Файл или директория не существует',
            NotADirectoryError: 'Ошибка: Нужен флаг -r для директорий',
            IsADirectoryError: 'Ошибка: Это директория',
            shutil.SameFileError: 'Ошибка: Источник и назначение одинаковы',
            ValueError: 'Ошибка: Неверный запрос'
        }
        if exc_val and str(exc_val):
            print(f'Ошибка: {exc_val}')
        else:
            print(error_map.get(exc_type, 'Ошибка'))


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
