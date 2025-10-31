import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.cd import cd


def test_cd_nonexistent_directory(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        cd('nonexistent_dir')


def test_cd_file_instead_directory(fs: FakeFilesystem, home_dir) -> None:
    fs.create_file(home_dir / 'test_file.txt')
    with pytest.raises(NotADirectoryError):
        cd('test_file.txt')


def test_cd_absolute_path(fs: FakeFilesystem) -> None:
    fs.create_dir('/test/dir')
    result = cd('/test/dir')
    assert result == 'Успешно'


def test_cd_relative_path(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(home_dir / 'subdir')
    result = cd('subdir')
    assert result == 'Успешно'


def test_cd_home_directory(fs: FakeFilesystem) -> None:
    result = cd('~')
    assert result == 'Успешно'


def test_cd_parent_directory(fs: FakeFilesystem) -> None:
    result = cd('..')
    assert result == 'Успешно'


def test_cd_current_directory(fs: FakeFilesystem) -> None:
    result = cd('.')
    assert result == 'Успешно'


def test_cd_empty_path(fs: FakeFilesystem) -> None:
    result = cd()
    assert result == 'Успешно'


def test_cd_with_tilde_expansion(fs: FakeFilesystem, home_dir) -> None:
    fs.create_dir(str(home_dir / 'documents'))
    result = cd(str(home_dir / 'documents'))
    assert result == 'Успешно'