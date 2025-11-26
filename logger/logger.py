"""
Модуль для настройки логгера
"""
import logging.config
from pathlib import Path
import datetime

import yaml
from configs.config import *
from utils.validator import ensure_dir_exists

logger = logging.getLogger(__name__)

def setup_logging(write_logs_into_file: bool = True) -> None:
    """
    Настройка логгера с проверкой наличия конфига для него
    """

    # Инициализирую простейший логер, который возьмет на себя работу, если будут проблемы с конфигурацией логгера
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    temp_logger = logging.getLogger("bootstrap")

    cfg_path = Path(LOGGING_CONFIG_PATH)

    # Проверка, что файл конфигурации логгера существует. Создание при необходимости
    ensure_dir_exists(cfg_path, create_if_missing=CREATE_MISSING_DIRS)

    # Читаем конфиг логгера
    with open(LOGGING_CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    if write_logs_into_file:
        temp_logger.info("Включена запись логов в файл, проверка существования директории для логов")
        logs_dir_path = Path(LOGGING_DIR_PATH)

        # Проверка, что директория для логов существует. Создание при необходимости
        ensure_dir_exists(logs_dir_path, create_if_missing=CREATE_MISSING_DIRS)

        # Добавляем в конфиг логгера путь к файлу логов
        config["handlers"]["file"]["filename"] = str(LOGGING_FILE_PATH)

        # Инициализируем полноценный конфиг логгера, который может писать в файл
        try:
            logging.config.dictConfig(config)
        except Exception as e:
            temp_logger.critical(f"Проблемы с файлом конфигурации, запись логов в файл невозможна: {e}, завершение работы программы")
            raise SystemExit(1)
    else:
        try:
            logging.config.dictConfig(config)
        except Exception as e:
            temp_logger.error(f"Проблемы с файлом конфигурации, будет использоваться стандартный логгер: {e}")

    logging.info(f"-------- Запуск программы {datetime.datetime.now()} --------")