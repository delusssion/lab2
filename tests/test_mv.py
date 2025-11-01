import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.mv import mv


def test_nonexistent_source(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        mv('nonexistent.txt', 'new_location.txt')


def test_rename_file(fs: FakeFilesystem) -> None:
    content = 'test content'
    fs.create_file('old_name.txt', contents=content)

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = mv('old_name.txt', 'new_name.txt')

    assert result == 'Успешно'
    assert not os.path.exists('old_name.txt')
    assert os.path.exists('new_name.txt')
    with open('new_name.txt', 'r') as f:
        assert f.read() == content


def test_file_to_dir(fs: FakeFilesystem) -> None:
    content = 'test content'
    fs.create_file('file.txt', contents=content)
    fs.create_dir('target_dir')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = mv('file.txt', 'target_dir')

    assert result == 'Успешно'
    assert not os.path.exists('file.txt')
    assert os.path.exists('target_dir/file.txt')


def test_move_dir(fs: FakeFilesystem) -> None:
    fs.create_dir('old_dir/subdir')
    fs.create_file('old_dir/file.txt', contents='content')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = mv('old_dir', 'new_dir')

    assert result == 'Успешно'
    assert not os.path.exists('old_dir')
    assert os.path.exists('new_dir/file.txt')


def test_overwrite_file(fs: FakeFilesystem) -> None:
    fs.create_file('new.txt', contents='new content')
    fs.create_file('old.txt', contents='old content')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = mv('new.txt', 'old.txt')

    assert result == 'Успешно'
    assert not os.path.exists('new.txt')
    with open('old.txt', 'r') as f:
        assert f.read() == 'new content'


def test_self_move(fs: FakeFilesystem) -> None:
    fs.create_dir('source_dir/subdir')
    with pytest.raises(ValueError):
        mv('source_dir', 'source_dir/copy')


def test_to_existing_dir(fs: FakeFilesystem) -> None:
    fs.create_file('file.txt', contents='content')
    fs.create_dir('existing_dir')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = mv('file.txt', 'existing_dir')

    assert result == 'Успешно'
    assert os.path.exists('existing_dir/file.txt')
