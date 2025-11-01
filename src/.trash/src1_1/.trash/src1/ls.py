from pathlib import Path
from datetime import datetime
from errors import CommandContext, validate_path_exists


def format_size(size):
    '''Форматирует размер файла в читаемый вид'''
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024 or unit == 'T':
            return f'{size:.1f}{unit}'
        size /= 1024
    return f'{size:.1f}T'


def ls(path='.', long_format=False):
    '''Отображает содержимое директории'''
    with CommandContext():
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
                    'modified': stats.st_mtime
                })
            except OSError:
                continue

        file_list.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

        if long_format:
            for item in file_list:
                size_display = '<DIR>' if item['is_dir'] else format_size(item['size'])
                date_str = datetime.fromtimestamp(item['modified']).strftime('%d %b %H:%M')
                file_type = 'd' if item['is_dir'] else '-'
                print(f"{file_type} {size_display:>8} {date_str} {item['name']}")
        else:
            for item in file_list:
                print(item['name'])
