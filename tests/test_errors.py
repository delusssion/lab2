import pytest
from src.errors import validate_path_exists, validate_is_file, validate_is_directory
import tempfile

def test_path_exists():
    with tempfile.NamedTemporaryFile() as tmp:
        validate_path_exists(tmp.name)

    with pytest.raises(FileNotFoundError):
        validate_path_exists('/nonexistent/path')


def test_is_file():
    with tempfile.NamedTemporaryFile() as tmp:
        validate_is_file(tmp.name)

    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(IsADirectoryError):
            validate_is_file(tmp)


def test_is_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        validate_is_directory(tmp_dir)

    with tempfile.NamedTemporaryFile() as tmp_file:
        with pytest.raises(NotADirectoryError):
            validate_is_directory(tmp_file.name)
