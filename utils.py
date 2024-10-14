from pathlib import Path

class Utilities:
    @staticmethod
    def is_valid_path(path: str) -> bool:
        """Проверяет, является ли путь валидным каталогом."""
        return Path(path).exists() and Path(path).is_dir()