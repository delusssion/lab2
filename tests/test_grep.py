import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.grep import grep


def test_grep_nonexistent_path(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        grep('pattern', 'nonexistent.txt')


def test_grep_in_file(fs: FakeFilesystem) -> None:
    content = 'first line\nmatch here\nlast line'
    fs.create_file('test.txt', contents=content)
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = grep('match', 'test.txt')
    
    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'match here' in output
    assert 'test.txt' in output


def test_grep_no_matches(fs: FakeFilesystem) -> None:
    fs.create_file('test.txt', contents='hello\nworld')
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = grep('nonexistent', 'test.txt')
    
    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'Совпадений не найдено' in output


def test_grep_recursive(fs: FakeFilesystem) -> None:
    fs.create_dir('project')
    fs.create_file('project/file1.txt', contents='find me')
    fs.create_dir('project/subdir')
    fs.create_file('project/subdir/file2.txt', contents='find me too')
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = grep('find', 'project', recursive=True)
    
    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'file1.txt' in output
    assert 'file2.txt' in output


def test_grep_ignore_case(fs: FakeFilesystem) -> None:
    fs.create_file('test.txt', contents='CaseSensitive')
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = grep('casesensitive', 'test.txt', ignore_case=True)
    
    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'CaseSensitive' in output


def test_grep_multiple_matches(fs: FakeFilesystem) -> None:
    content = 'match first\nno match\nmatch second'
    fs.create_file('test.txt', contents=content)
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        result = grep('match', 'test.txt')
    
    assert result == 'Успешно'
    output = '\n'.join(str(p) for p in printed)
    assert 'match first' in output
    assert 'match second' in output
    assert 'no match' in output


def test_grep_regex_pattern(fs: FakeFilesystem) -> None:
    content = '123-45-6789\nphone: 555-1234'
    fs.create_file('data.txt', contents=content)
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        grep(r'\d{3}-\d{2}-\d{4}', 'data.txt')
    
    output = '\n'.join(str(p) for p in printed)
    assert '123-45-6789' in output
    assert '555-1234' not in output


def test_grep_multiple_files(fs: FakeFilesystem) -> None:
    fs.create_file('file1.txt', contents='hello world')
    fs.create_file('file2.txt', contents='hello there')
    fs.create_file('file3.txt', contents='goodbye')
    
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        grep('hello', '.', recursive=True)
    
    output = '\n'.join(str(p) for p in printed)
    assert 'file1.txt' in output
    assert 'file2.txt' in output
    assert 'file3.txt' not in output