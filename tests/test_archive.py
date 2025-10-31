import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.archive import zip_folder, tar_folder, unzip_archive, untar_archive


def test_zip_nonexistent_folder(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        zip_folder('nonexistent_folder')


def test_zip_file_instead_folder(fs: FakeFilesystem) -> None:
    fs.create_file('test_file.txt')
    with pytest.raises(ValueError):
        zip_folder('test_file.txt')


def test_zip_folder(fs: FakeFilesystem) -> None:
    fs.create_dir('source')
    fs.create_file('source/file1.txt', contents='content1')
    fs.create_file('source/file2.txt', contents='content2')
    
    result = zip_folder('source', 'archive.zip')
    assert result == 'Успешно'
    assert os.path.exists('archive.zip')


def test_zip_folder_default_name(fs: FakeFilesystem) -> None:
    fs.create_dir('my_folder')
    fs.create_file('my_folder/file.txt', contents='content')
    
    result = zip_folder('my_folder')
    assert result == 'Успешно'
    assert os.path.exists('my_folder.zip')


def test_unzip_archive(fs: FakeFilesystem) -> None:
    fs.create_dir('source')
    fs.create_file('source/file1.txt', contents='content1')
    fs.create_file('source/file2.txt', contents='content2')
    zip_folder('source', 'archive.zip')

    result = unzip_archive('archive.zip')
    assert result == 'Успешно'
    assert os.path.exists('source/file1.txt')
    assert os.path.exists('source/file2.txt')


def test_unzip_nonexistent_archive(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        unzip_archive('nonexistent.zip')


def test_tar_folder(fs: FakeFilesystem) -> None:
    fs.create_dir('data')
    fs.create_file('data/info.txt', contents='data content')
    
    result = tar_folder('data', 'data.tar.gz')
    assert result == 'Успешно'
    assert os.path.exists('data.tar.gz')


def test_untar_archive(fs: FakeFilesystem) -> None:
    fs.create_dir('source')
    fs.create_file('source/document.txt', contents='document content')
    fs.create_dir('source/subdir')
    fs.create_file('source/subdir/config.txt', contents='config content')
    tar_folder('source', 'source.tar.gz')

    result = untar_archive('source.tar.gz')
    assert result == 'Успешно'
    assert os.path.exists('source/document.txt')
    assert os.path.exists('source/subdir/config.txt')


def test_untar_nonexistent_archive(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        untar_archive('nonexistent.tar.gz')


def test_zip_folder_with_subdirectories(fs: FakeFilesystem) -> None:
    fs.create_dir('project/src')
    fs.create_dir('project/docs')
    fs.create_file('project/src/main.py', contents="print('hello')")
    fs.create_file('project/docs/readme.md', contents='# Documentation')
    fs.create_file('project/.gitignore', contents='*.pyc')
    
    result = zip_folder('project', 'project.zip')
    assert result == 'Успешно'
    assert os.path.exists('project.zip')


def test_tar_folder_with_subdirectories(fs: FakeFilesystem) -> None:
    fs.create_dir('app/static')
    fs.create_dir('app/templates')
    fs.create_file('app/main.py', contents='code')
    fs.create_file('app/static/style.css', contents='css')
    fs.create_file('app/templates/index.html', contents='html')
    
    result = tar_folder('app', 'app.tar.gz')
    assert result == 'Успешно'
    assert os.path.exists('app.tar.gz')