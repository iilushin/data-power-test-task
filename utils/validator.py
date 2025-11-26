"""
Модуль, который реализует валидацию путей файлов или директорий
"""

import logging
from pathlib import Path

from configs.config import INIT_TABLE_COLUMNS, DEDUPLICATE_DATA_BY_COLUMNS

logger = logging.getLogger(__name__)

class PathValidationError(Exception):
    """Ошибка валидации путей файлов или директорий"""
    pass


class ConfigValidationError(Exception):
    """Ошибка валидации конфигов"""
    pass


def ensure_dir_exists(path: str | Path,
                      create_if_missing: bool = False) -> None:
    """
    Проверяет, что директория существует и путь указывает именно на директорию
    Если не существует и create_if_missing=True — создаёт директорию
    Иначе — выбрасывает ошибку
    """
    p = Path(path)

    if not p.exists():
        if create_if_missing:
            try:
                p.mkdir(parents=True, exist_ok=True)
                msg = f"Директория {p} не существовала и была создана"
                logger.info(msg)
                return
            except Exception as e:
                msg = f"Ошибка создания директории {p}: {e}"
                logger.error(msg)
                raise PathValidationError(msg)
        else:
            msg = f"Директория {p} не существует"
            logger.error(msg)
            raise PathValidationError(msg)


def ensure_file_exists(path: str | Path) -> None:
    """
    Проверяет, что файл существует
    """
    p = Path(path)

    if not p.exists():
        msg = f"Файл {p} не существует"
        logger.error(msg)
        raise PathValidationError(msg)


def validate_paths(config: dict,
                   create_missing_dirs: bool = False) -> None:
    """
    Валидирует директории и файлы
    Можно включить создание недостающих директорий
    """

    if create_missing_dirs:
        logger.info("Валидация директорий и файлов, недостающие директории будут созданы...")
    else:
        logger.info("Валидация директорий и файлов...")

    for d in config.get("dirs", []):
        ensure_dir_exists(d, create_if_missing=create_missing_dirs)

    for f in config.get("files", []):
        ensure_file_exists(f)


def validate_config() -> None:
    """
    Проверка, что поля для дедупликации есть в таблице
    """
    logger.info("Валидация конфига для таблицы")
    if DEDUPLICATE_DATA_BY_COLUMNS:
        for c in DEDUPLICATE_DATA_BY_COLUMNS:
            if c not in INIT_TABLE_COLUMNS.keys():
                msg = f"Проверьте файл конфигурации: поля {c} для дедупликации нет в таблице"
                logging.error(msg)
                raise ConfigValidationError(msg)
    else: return