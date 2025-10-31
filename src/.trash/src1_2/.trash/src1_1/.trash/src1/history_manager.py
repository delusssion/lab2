import json
import shutil
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path(__file__).parent / '.history'
TRASH_DIR = Path(__file__).parent / '.trash'


class HistoryManager:
    def __init__(self):
        self.history_file = HISTORY_FILE
        self.trash_dir = TRASH_DIR
        self.history = []
        self.load_history()
        self.trash_dir.mkdir(exist_ok=True)
    
    def load_history(self):
        '''Загружает историю из файла'''
        if self.history_file.exists():
            try:
                self.history = json.loads(self.history_file.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, Exception):
                self.history = []
    
    def save_history(self):
        '''Сохраняет историю в файл'''
        self.history_file.write_text(
            json.dumps(self.history[-100:], ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def add_command(self, command, operation_type=None, source=None, destination=None):
        '''Добавляет команду в историю'''
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'type': operation_type,
            'source': source,
            'destination': destination
        }
        self.history.append(entry)
        self.save_history()
    
    def show_history(self, count=10):
        '''Показывает историю команд'''
        if not self.history:
            print('История пуста')
            return
        
        recent = self.history[-count:] if count else self.history
        print(f'Последние {len(recent)} команд:')
        
        for i, entry in enumerate(recent, 1):
            idx = len(self.history) - len(recent) + i
            time = entry['timestamp'][11:19]
            print(f"{idx}. [{time}] {entry['command']}")
    
    def undo_last(self):
        '''Отменяет последнюю операцию'''
        if not self.history:
            msg = 'Ошибка: Нет команд для отмены'
            print(msg)
            return msg
        
        for i in range(len(self.history) - 1, -1, -1):
            entry = self.history[i]
            if entry['type'] in ['cp', 'mv', 'rm']:
                return self.undo_operation(entry, i)
        
        msg = 'Ошибка: Нет операций для отмены (в истории только команды чтения)'
        print(msg)
        return msg
    
    def undo_operation(self, entry, index):
        '''Отменяет конкретную операцию'''
        try:
            op_type = entry['type']
            src, dst = entry.get('source'), entry.get('destination')
            
            if op_type == 'cp' and dst and Path(dst).exists():
                safe_remove(Path(dst))
                print(f'Отменено копирование: удален {dst}')
            
            elif op_type == 'mv' and src and dst:
                if Path(dst).exists():
                    shutil.move(dst, src)
                    print(f'Отменено перемещение: {dst} → {src}')
            
            elif op_type == 'rm' and src:
                trash_path = self.trash_dir / Path(src).name
                
                if trash_path.exists():
                    if Path(src).exists():
                        counter = 1
                        while True:
                            new_path = Path(src).parent / f'{Path(src).stem}_{counter}{Path(src).suffix}'
                            if not new_path.exists():
                                shutil.move(str(trash_path), str(new_path))
                                print(f'Восстановлено как: {new_path.name}')
                                break
                            counter += 1
                    else:
                        shutil.move(str(trash_path), src)
                        print(f'Восстановлено: {src}')
            
            self.history.pop(index)
            self.save_history()
            return 'Успешно'
        
        except Exception as e:
            msg = f'Ошибка при отмене: {e}'
            print(msg)
            return msg


history_manager = HistoryManager()


def show_history(count=10):
    '''Показывает историю команд'''
    history_manager.show_history(count)
    return 'Успешно'


def undo_last():
    '''Отменяет последнюю операцию'''
    return history_manager.undo_last()


def safe_remove(path):
    '''Безопасно удаляет файл или директорию (перемещает в корзину)'''
    path_obj = Path(path)
    trash_path = TRASH_DIR / path_obj.name
    
    counter = 1
    while trash_path.exists():
        trash_path = TRASH_DIR / f'{path_obj.stem}_{counter}{path_obj.suffix}'
        counter += 1
    shutil.move(str(path_obj), str(trash_path))


def clear_trash():
    '''Очищает корзину (.trash)'''
    try:
        if TRASH_DIR.exists():
            shutil.rmtree(TRASH_DIR)
            TRASH_DIR.mkdir(exist_ok=True)
            return 'Корзина очищена'
        return 'Корзина пуста'
    except Exception as e:
        return f'Ошибка при очистке: {e}'