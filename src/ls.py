from pathlib import Path
from datetime import datetime
from errors import validate_path_exists
import stat
from constants import DATE_FORMAT

def format_size(size: int) -> str:
    '''Форматирует размер файла в читаемый вид'''
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024 or unit == 'T':
            return f'{size:.1f}{unit}'
        size /= 1024
    return f'{size:.1f}T'

def get_permissions(mode: int) -> str:
    '''Преобразует числовые права доступа в строку типа "drwxr-xr-x"'''
    if stat.S_ISDIR(mode):
        permissions = 'd'
    elif stat.S_ISLNK(mode):
        permissions = 'l'
    else:
        permissions = '-'

    permissions += 'r' if mode & stat.S_IRUSR else '-'
    permissions += 'w' if mode & stat.S_IWUSR else '-'
    permissions += 'x' if mode & stat.S_IXUSR else '-'

    permissions += 'r' if mode & stat.S_IRGRP else '-'
    permissions += 'w' if mode & stat.S_IWGRP else '-'
    permissions += 'x' if mode & stat.S_IXGRP else '-'

    permissions += 'r' if mode & stat.S_IROTH else '-'
    permissions += 'w' if mode & stat.S_IWOTH else '-'
    permissions += 'x' if mode & stat.S_IXOTH else '-'

    return permissions

def ls(path: str = '.', long_format: bool = False) -> None:
    '''Отображает содержимое директории'''
    folder_path = Path(path)
    validate_path_exists(folder_path)

    file_list = []
    for item in folder_path.iterdir():
        try:
            stats = item.stat()
            file_list.append({
                'name': item.name,
                'is_dir': item.is_dir(),
                'size': stats.st_size,
                'modified': stats.st_mtime,
                'mode': stats.st_mode,
                'permissions': get_permissions(stats.st_mode)
            })
        except OSError:
            continue

    file_list.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

    if long_format:
        for item in file_list:
            size_display = '<DIR>' if item['is_dir'] else format_size(item['size'])
            date_str = datetime.fromtimestamp(item['modified']).strftime(DATE_FORMAT)
            print(f"{item['permissions']} {size_display:>8} {date_str} {item['name']}")
    else:
        for item in file_list:
            print(item['name'])
