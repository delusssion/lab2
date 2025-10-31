import pytest
from src.history_manager import show_history, undo_last


def test_show_history(fs) -> None:
    with pytest.MonkeyPatch().context() as m:
        printed = []
        m.setattr('builtins.print', lambda x: printed.append(x))
        
        result = show_history()
        
        assert result == 'Успешно'
        assert len(printed) > 0


def test_undo_no_operations(fs) -> None:
    from src.history_manager import history_manager
    history_manager.history = []
    history_manager.save_history()
    
    result = undo_last()
    print(f'DEBUG: undo_last returned: {result}')