from pathlib import Path
from errors import validate_path_exists, validate_is_file
from constants import MAX_FILE_SIZE


def cat(file_path: str) -> str:
    '''Выводит содержимое файла'''
    path_obj = Path(file_path)
    validate_path_exists(path_obj)
    validate_is_file(path_obj)
    
    if path_obj.stat().st_size > MAX_FILE_SIZE:
        raise ValueError('Файл слишком большой')
    
    print(path_obj.read_text(encoding='utf-8'))
    return 'Успешно'