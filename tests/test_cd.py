import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.cd import cd


def test_nonexistent_dir(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        cd('nonexistent_dir')


def test_file_instead_dir(fs: FakeFilesystem, home_dir) -> None:
    fs.create_file(home_dir / 'test_file.txt')
    with pytest.raises(NotADirectoryError):
        cd('test_file.txt')


def test_absolute_path(fs: FakeFilesystem) -> None:
    fs.create_dir('/test/dir')
    result = cd('/test/dir')
    assert result == 'Успешно'


def test_relative_path(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(home_dir / 'subdir')
    result = cd('subdir')
    assert result == 'Успешно'


def test_home_dir(fs: FakeFilesystem) -> None:
    result = cd('~')
    assert result == 'Успешно'


def test_parent_dir(fs: FakeFilesystem) -> None:
    result = cd('..')
    assert result == 'Успешно'


def test_current_dir(fs: FakeFilesystem) -> None:
    result = cd('.')
    assert result == 'Успешно'


def test_empty_path(fs: FakeFilesystem) -> None:
    result = cd()
    assert result == 'Успешно'


def test_tilde_expansion(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(str(home_dir / 'documents'))
    result = cd(str(home_dir / 'documents'))
    assert result == 'Успешно'
