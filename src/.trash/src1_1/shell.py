# shell.py
import os
from logsetup import setup_logging
from ls import ls
from cd import cd
from cat import cat
from cp import cp
from mv import mv
from rm import rm
from archive import zip_folder, unzip_archive, tar_folder, untar_archive
from grep import grep
from history_manager import show_history, undo_last, history_manager, clear_trash


logger = setup_logging()

def parse_flags(args, flags):
    '''Парсит флаги из аргументов'''
    found_flags = {flag: flag in args for flag in flags}
    clean_args = [a for a in args if a not in flags]
    return found_flags, clean_args

def execute_command(command, cmd, args):
    '''Выполняет команду'''
    result = None
    try:
        if cmd == 'ls':
            flags, clean_args = parse_flags(args, ['-l'])
            path = clean_args[0] if clean_args else '.'
            ls(path, flags['-l'])
            result = 'Успешно'

        elif cmd == 'cd':
            result = cd(args[0] if args else None)

        elif cmd == 'cat':
            if not args:
                raise ValueError('файл не указан')
            result = cat(args[0])

        elif cmd == 'cp':
            if len(args) < 2:
                raise ValueError('неверные аргументы')
            flags, clean_args = parse_flags(args, ['-r'])
            if len(clean_args) < 2:
                raise ValueError('неверные аргументы')

            history_manager.add_command(command, 'cp', source=clean_args[0], destination=clean_args[1])
            result = cp(clean_args[0], clean_args[1], flags['-r'])

        elif cmd == 'mv':
            if len(args) < 2:
                raise ValueError('неверные аргументы')
            history_manager.add_command(command, 'mv', source=args[0], destination=args[1])
            result = mv(args[0], args[1])

        elif cmd == 'rm':
            if not args:
                raise ValueError('цель не указана')
            flags, clean_args = parse_flags(args, ['-r'])
            if not clean_args:
                raise ValueError('цель не указана')

            history_manager.add_command(command, 'rm', source=clean_args[0])
            result = rm(clean_args[0], recursive=flags['-r'])

        elif cmd == 'zip':
            if len(args) == 1:
                result = zip_folder(args[0])
                print(result)
            elif len(args) == 2:
                result = zip_folder(args[0], args[1])
                print(result)
            else:
                raise ValueError('неверное использование команды. Делай так: zip <папка> [<архив.zip>]')

        elif cmd == 'unzip':
            if len(args) != 1:
                raise ValueError('неверное использование команды. Делай так: unzip <архив.zip>')
            result = unzip_archive(args[0])
            print(result)

        elif cmd == 'tar':
            if len(args) != 2:
                raise ValueError('неверное использование команды. Делай так: tar <папка> <архив.tar.gz>')
            result = tar_folder(args[0], args[1])
            print(result)

        elif cmd == 'untar':
            if len(args) != 1:
                raise ValueError('неверное использование команды. Делай так: untar <архив.tar.gz>')
            result = untar_archive(args[0])
            print(result)

        elif cmd == 'grep':
            if len(args) < 2:
                raise ValueError('неверное использование команды. Делай так: grep [опции] <шаблон> <путь>')
            flags, clean_args = parse_flags(args, ['-r', '-i'])
            if len(clean_args) < 2:
                raise ValueError('неверное использование команды. Делай так: grep [опции] <шаблон> <путь>')
            result = grep(clean_args[0], clean_args[1], flags['-r'], flags['-i'])

        elif cmd == 'history':
            count = int(args[0]) if args else 10
            show_history(count)
            result = 'Успешно'

        elif cmd == 'undo':
            result = undo_last()
            print(result)

        elif cmd == 'clear_trash':
            result = clear_trash()
            print(result)

        else:
            raise ValueError(f'Неизвестная команда: {cmd}')

    except Exception as e:
        print(f'Ошибка: {e}')
        logger.error(f'CMD: {command} | ERROR: {e}')
        return f'Ошибка: {e}'

    if result is None:
        logger.error(f'CMD: {command} | ERROR: команда не вернула результат')
        return 'Ошибка'

    logger.info(f'CMD: {command} | RESULT: {result}')
    return result


# shell.py (исправленная часть main())
def main():
    '''Основная функция shell'''
    print('Консольный Shell. Для завершения работы программы напиши "exit".')
    print('Доступные команды: ls, cd, cat, cp, mv, rm, zip, unzip, tar, untar, grep, history, undo, clear_trash')

    while True:
        try:
            cwd = os.getcwd()
            command = input('{0} >>> '.format(cwd)).strip()
            if not command:
                continue
            if command == 'exit':
                break

            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            # Сохраняем в историю только команды, которые НЕ сохраняются в execute_command
            if cmd not in ['cp', 'mv', 'rm']:
                history_manager.add_command(command)

            execute_command(command, cmd, args)

        except KeyboardInterrupt:
            print('\nИспользуйте "exit" для выхода')
        except EOFError:
            print('\nВыход')
            break

    print('Завершение работы Shell.')
