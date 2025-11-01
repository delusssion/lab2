import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.cat import cat


def test_nonexistent_file(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        cat('nonexisting.txt')


def test_directory_instead_file(fs: FakeFilesystem) -> None:
    fs.create_dir('test_dir')
    with pytest.raises(IsADirectoryError):
        cat('test_dir')


def test_file_content(fs: FakeFilesystem, home_dir) -> None:
    content = 'hello\nworld'
    path = str(home_dir / 'test.txt')
    fs.create_file(path, contents=content)

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = cat(path)

    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'hello' in output
    assert 'world' in output


def test_large_file(fs: FakeFilesystem) -> None:
    large_content = 'x' * (11 * 1024 * 1024)
    fs.create_file('large.txt', contents=large_content)
    with pytest.raises(ValueError):
        cat('large.txt')


def test_empty_file(fs: FakeFilesystem) -> None:
    fs.create_file('empty.txt', contents='')

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = cat('empty.txt')

    assert result == 'Успешно'
    assert len(printed) == 0 or printed == ['']


def test_special_chars(fs: FakeFilesystem) -> None:
    content = 'тест\n中文\n🧠'
    fs.create_file('special.txt', contents=content)

    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = cat('special.txt')

    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'тест' in output
    assert '中文' in output
