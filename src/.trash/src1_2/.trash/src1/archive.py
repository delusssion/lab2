import zipfile
import tarfile
import sys
from pathlib import Path
from errors import CommandContext, validate_path_exists


def zip_folder(folder_path, archive_name=None):
    '''Создает ZIP архив из папки'''
    with CommandContext():
        folder = Path(folder_path)
        validate_path_exists(folder)
        
        if not folder.is_dir():
            raise ValueError(f"'{folder_path}' не является папкой")

        if not archive_name:
            archive_name = f"{folder.name}.zip"
        
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_item in folder.rglob('*'):
                if file_item.is_file():
                    zip_file.write(file_item, file_item.relative_to(folder))
        
        return 'Успешно'


def unzip_archive(archive_path):
    '''Распаковывает ZIP архив'''
    with CommandContext():
        archive = Path(archive_path)
        validate_path_exists(archive)
        
        with zipfile.ZipFile(archive, 'r') as zip_file:
            zip_file.extractall()
        
        return 'Успешно'


def tar_folder(folder_path, archive_name):
    '''Создает TAR.GZ архив из папки'''
    with CommandContext():
        folder = Path(folder_path)
        validate_path_exists(folder)
        
        if not folder.is_dir():
            raise ValueError(f"'{folder_path}' не является папкой")
        
        with tarfile.open(archive_name, 'w:gz') as tar_file:
            tar_file.add(folder, arcname=folder.name)
        
        return 'Успешно'


def untar_archive(archive_path):
    '''Распаковывает TAR.GZ архив'''
    with CommandContext():
        archive = Path(archive_path)
        validate_path_exists(archive)
        
        with tarfile.open(archive, 'r:gz') as tar_file:
            try:
                tar_file.extractall(filter='data')
            except TypeError:
                tar_file.extractall()
        
        return 'Успешно'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Использование:')
        print('  python3 archive.py zip <папка> <архив.zip>')
        print('  python3 archive.py unzip <архив.zip>')
        print('  python3 archive.py tar <папка> <архив.tar.gz>')
        print('  python3 archive.py untar <архив.tar.gz>')
        sys.exit(1)
    
    cmd = sys.argv[1]
    commands = {
        'zip': (zip_folder, 4),
        'unzip': (unzip_archive, 3),
        'tar': (tar_folder, 4),
        'untar': (untar_archive, 3)
    }
    
    if cmd not in commands:
        print(f'Неизвестная команда: {cmd}')
        sys.exit(1)
    
    func, expected_args = commands[cmd]
    
    if len(sys.argv) != expected_args:
        print(f'Неверное количество аргументов для команды {cmd}')
        sys.exit(1)
    
    result = func(*sys.argv[2:])
    print(result)