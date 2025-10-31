from pathlib import Path
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
import os


@pytest.fixture(autouse=True)
def setup_fs(fs: FakeFilesystem, monkeypatch) -> dict:
    '''Автоматически настраивает fake filesystem для всех тестов'''
    home_dir = Path('/home/testuser')
    fs.create_dir(str(home_dir))

    lab_dir = Path('/Users/delusionn/prog/labs/lab2')
    fs.create_dir(str(lab_dir))
    fs.create_dir(str(lab_dir / 'src'))
    
    monkeypatch.setattr(Path, 'home', staticmethod(lambda: home_dir))
    monkeypatch.setattr(os, 'getcwd', lambda: str(home_dir))
    
    chdir_calls = []
    monkeypatch.setattr(os, 'chdir', lambda path: chdir_calls.append(str(path)))
    monkeypatch.setattr(Path, 'cwd', lambda: home_dir)
    
    return {
        'home_dir': home_dir,
        'chdir_calls': chdir_calls
    }


@pytest.fixture
def home_dir(setup_fs) -> Path:
    return setup_fs['home_dir']


@pytest.fixture
def chdir_calls(setup_fs) -> list:
    return setup_fs['chdir_calls']