import os
from pathlib import Path
from errors import CommandContext, validate_path_exists, validate_is_directory


def cd(path=None):
    '''Изменяет текущую рабочую директорию'''
    with CommandContext():
        if not path or path == '~':
            new_path = Path.home()
        elif path == '..':
            new_path = Path.cwd().parent
        else:
            new_path = Path(path).expanduser().resolve()
            validate_path_exists(new_path)
            validate_is_directory(new_path)
        
        os.chdir(new_path)
        return 'Успешно'