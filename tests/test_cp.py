import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.cp import cp


def test_nonexistent_source(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        cp('nonexistent.txt', 'copy.txt')


def test_copy_file(fs: FakeFilesystem) -> None:
    content = 'test content'
    fs.create_file('source.txt', contents=content)

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = cp('source.txt', 'destination.txt')

    assert result == 'Успешно'
    assert os.path.exists('destination.txt')
    with open('destination.txt', 'r') as f:
        assert f.read() == content


def test_dir_without_recursive(fs: FakeFilesystem) -> None:
    fs.create_dir('source_dir')
    with pytest.raises(NotADirectoryError):
        cp('source_dir', 'dest_dir')


def test_recursive_copy(fs: FakeFilesystem) -> None:
    fs.create_dir('source_dir/subdir')
    fs.create_file('source_dir/file1.txt', contents='content1')
    fs.create_file('source_dir/subdir/file2.txt', contents='content2')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = cp('source_dir', 'dest_dir', recursive=True)

    assert result == 'Успешно'
    assert os.path.exists('dest_dir/file1.txt')
    assert os.path.exists('dest_dir/subdir/file2.txt')


def test_file_to_dir(fs: FakeFilesystem) -> None:
    fs.create_file('file.txt', contents='content')
    fs.create_dir('target_dir')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = cp('file.txt', 'target_dir')

    assert result == 'Успешно'
    assert os.path.exists('target_dir/file.txt')


def test_overwrite_file(fs: FakeFilesystem) -> None:
    fs.create_file('source.txt', contents='new content')
    fs.create_file('existing.txt', contents='old content')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        result = cp('source.txt', 'existing.txt')

    assert result == 'Успешно'
    with open('existing.txt', 'r') as f:
        assert f.read() == 'new content'


def test_self_copy(fs: FakeFilesystem) -> None:
    fs.create_dir('source_dir/subdir')
    with pytest.raises(ValueError):
        cp('source_dir', 'source_dir/copy', recursive=True)


def test_multiple_files(fs: FakeFilesystem) -> None:
    fs.create_file('file1.txt', contents='content1')
    fs.create_file('file2.txt', contents='content2')
    fs.create_dir('backup')

    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.print', lambda x: None)
        cp('file1.txt', 'backup')
        cp('file2.txt', 'backup')

    assert os.path.exists('backup/file1.txt')
    assert os.path.exists('backup/file2.txt')
