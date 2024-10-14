import os
import psutil

class OnScreenKeyboard:

    @staticmethod
    def is_running() -> bool:
        """Проверяет, запущена ли экранная клавиатура."""
        return any(proc.info['name'] == 'osk.exe' for proc in psutil.process_iter(['name']))

    @staticmethod
    def open() -> None:
        """Запускает экранную клавиатуру."""
        if not OnScreenKeyboard.is_running():
            try:
                os.startfile("osk")
            except Exception as e:
                print(f"Ошибка при запуске экранной клавиатуры: {e}")
    
    @staticmethod
    def close() -> None:
        """Принудительно закрывает экранную клавиатуру."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'osk.exe':
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    print(f"Не удалось закрыть экранную клавиатуру: {e}")
                break
