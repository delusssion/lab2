from pathlib import Path
from errors import validate_path_exists
from constants import PROTECTED_DIRS

def rm(target: str, recursive: bool = False) -> str:
    '''Удаляет файл или директорию'''
    target_path = Path(target).expanduser().resolve()
    validate_path_exists(target_path)
    
    if target_path.resolve() in PROTECTED_DIRS:
        raise ValueError('Нельзя удалять системные директории')
    
    if target_path.is_dir():
        if not recursive:
            raise ValueError('Используйте -r для удаления директорий')

        while True:
            user_input = input(f'Удалить директорию "{target}" и всё её содержимое? (y/n): ').strip().lower()
            
            if user_input == 'y':
                break
            elif user_input == 'n':
                print('Отменено')
                return 'Отменено'
            else:
                print('Пожалуйста, введите "y" (да) или "n" (нет)')
        
        from history_manager import safe_remove
        safe_remove(target_path)
    else:
        from history_manager import safe_remove
        safe_remove(target_path)
    
    print('Успешно')
    return 'Успешно'
