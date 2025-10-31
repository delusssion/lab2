from pathlib import Path
from errors import CommandContext, validate_path_exists, validate_is_file


def cat(file_path):
    '''Выводит содержимое файла'''
    with CommandContext():
        if not file_path:
            raise ValueError('Файл не указан')
        
        path_obj = Path(file_path)
        validate_path_exists(path_obj)
        validate_is_file(path_obj)
        
        if path_obj.stat().st_size > 10 * 1024 * 1024:
            raise ValueError('Файл слишком большой')
        
        print(path_obj.read_text(encoding='utf-8'))
        return 'Успешно'