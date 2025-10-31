import shutil
from pathlib import Path
from errors import CommandContext, validate_path_exists, validate_not_self_copy


def mv(source, destination):
    '''Перемещает или переименовывает файл/директорию'''
    with CommandContext():
        if not source or not destination:
            raise ValueError('Источник и назначение обязательны')
        
        src_path = Path(source)
        dst_path = Path(destination)
        validate_path_exists(src_path)
        
        if src_path.is_dir():
            validate_not_self_copy(src_path, dst_path)
        
        if dst_path.exists() and dst_path.is_dir():
            dst_path = dst_path / src_path.name
        
        shutil.move(str(src_path), str(dst_path))
        print('Успешно')
        return 'Успешно'