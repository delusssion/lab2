from pathlib import Path
from errors import CommandContext, validate_path_exists


def rm(target, recursive=False):
    '''Удаляет файл или директорию'''
    with CommandContext():
        if not target:
            raise ValueError('Цель не указана')

        target_path = Path(target)
        validate_path_exists(target_path)

        if target_path.resolve() in [Path('/'), Path.home()]:
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
