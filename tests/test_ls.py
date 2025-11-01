import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.ls import ls


def test_nonexistent_dir(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        ls('nonexistent_dir')


def test_current_dir(fs: FakeFilesystem) -> None:
    fs.create_file('file1.txt')
    fs.create_file('file2.txt')
    fs.create_dir('subdir')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls()

    file_names = [str(p).strip() for p in printed]
    assert 'file1.txt' in file_names
    assert 'file2.txt' in file_names
    assert 'subdir' in file_names


def test_specific_dir(fs: FakeFilesystem) -> None:
    fs.create_dir('test_dir')
    fs.create_file('test_dir/file.txt')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls('test_dir')

    file_names = [str(p).strip() for p in printed]
    assert 'file.txt' in file_names


def test_long_format(fs: FakeFilesystem) -> None:
    fs.create_file('test.txt', contents='content')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls(long_format=True)

    output = '\n'.join(str(p) for p in printed)
    assert 'test.txt' in output
    assert '-' in output


def test_empty_dir(fs: FakeFilesystem) -> None:
    fs.create_dir('empty_dir')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls('empty_dir')

    assert len(printed) == 0


def test_hidden_files(fs: FakeFilesystem) -> None:
    fs.create_file('.hidden')
    fs.create_file('visible.txt')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls()

    file_names = [str(p).strip() for p in printed]
    assert '.hidden' in file_names
    assert 'visible.txt' in file_names


def test_sorting(fs: FakeFilesystem) -> None:
    fs.create_dir('dir_b')
    fs.create_file('file_a.txt')
    fs.create_dir('dir_a')
    fs.create_file('file_b.txt')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls()

    file_names = [str(p).strip() for p in printed]
    assert file_names.index('dir_a') < file_names.index('file_a.txt')
    assert file_names.index('dir_b') < file_names.index('file_b.txt')


def test_permissions(fs: FakeFilesystem) -> None:
    fs.create_file('regular_file.txt', contents='content')
    fs.create_dir('directory')
    fs.create_file('executable_script.sh', contents="#!/bin/bash\necho 'hello'")

    os.chmod('regular_file.txt', 0o644)
    os.chmod('directory', 0o755)
    os.chmod('executable_script.sh', 0o755)

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls(long_format=True)

    output = '\n'.join(str(p) for p in printed)
    assert 'drwxr-xr-x' in output
    assert '-rw-r--r--' in output
    assert '-rwxr-xr-x' in output
    assert 'directory' in output
    assert 'regular_file.txt' in output
    assert 'executable_script.sh' in output


def test_symlinks(fs: FakeFilesystem) -> None:
    fs.create_file('target_file.txt', contents='target content')
    fs.create_symlink('link_to_file', 'target_file.txt')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls(long_format=True)

    output = '\n'.join(str(p) for p in printed)
    assert 'l' in output
    assert 'link_to_file' in output


def test_permissions_format(fs: FakeFilesystem) -> None:
    fs.create_file('test_file.txt', contents='test')
    os.chmod('test_file.txt', 0o644)

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls(long_format=True)

    output_lines = [str(p) for p in printed]
    file_line = None
    for line in output_lines:
        if 'test_file.txt' in line:
            file_line = line
            break

    assert file_line is not None
    parts = file_line.split()
    assert len(parts) >= 4
    permissions = parts[0]
    assert len(permissions) == 10
    assert permissions.startswith('-')
    assert permissions == '-rw-r--r--'


def test_simple_mode(fs: FakeFilesystem) -> None:
    fs.create_file('file1.txt')
    fs.create_dir('dir1')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        ls()

    output = '\n'.join(str(p) for p in printed)
    assert 'file1.txt' in output
    assert 'dir1' in output
    assert 'drwx' not in output
    assert '-rw-' not in output
    assert 'lrwx' not in output
