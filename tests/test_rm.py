import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.rm import rm


def test_nonexistent_file(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        rm('nonexistent.txt')


def test_dir_without_recursive(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(str(home_dir / 'test_dir'))
    with pytest.raises(ValueError):
        rm(str(home_dir / 'test_dir'))


def test_remove_file(fs: FakeFilesystem, home_dir) -> None:
    fs.create_file(str(home_dir / 'test_file.txt'), contents='content')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = rm(str(home_dir / 'test_file.txt'))

    assert result == 'Успешно'


def test_recursive_delete(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(str(home_dir / 'test_dir' / 'subdir'))
    fs.create_file(str(home_dir / 'test_dir' / 'file.txt'), contents='content')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        m.setattr('builtins.input', lambda x: 'y')
        result = rm(str(home_dir / 'test_dir'), recursive=True)

    assert result == 'Успешно'


def test_cancel_delete(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(str(home_dir / 'test_dir'))

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        m.setattr('builtins.input', lambda x: 'n')
        result = rm(str(home_dir / 'test_dir'), recursive=True)

    assert result == 'Отменено'
    assert os.path.exists(str(home_dir / 'test_dir'))


def test_empty_dir(fs: FakeFilesystem, home_dir) -> None:
    dir_path = str(home_dir / 'empty_dir')
    fs.create_dir(dir_path)

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        m.setattr('builtins.input', lambda x: 'y')
        result = rm(dir_path, recursive=True)

    assert result == 'Успешно'


def test_multiple_files(fs: FakeFilesystem, home_dir) -> None:
    file1_path = str(home_dir / 'file1.txt')
    file2_path = str(home_dir / 'file2.txt')
    fs.create_file(file1_path)
    fs.create_file(file2_path)

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        rm(file1_path)
        rm(file2_path)

    assert not os.path.exists(file1_path)
    assert not os.path.exists(file2_path)


def test_system_dirs(fs: FakeFilesystem, home_dir) -> None:
    with pytest.raises(ValueError):
        rm('/')
    with pytest.raises(ValueError):
        rm(str(home_dir))
