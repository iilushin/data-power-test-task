import logging
from configs.config import *
from db.db import init_db, insert_data
from etl.etl import read_input_data, format_and_deduplicate_data
from logger.logger import setup_logging
from utils.validator import validate_paths, PathValidationError, validate_config

# Настройка логирования
setup_logging(write_logs_into_file=WRITE_LOGS_INTO_FILE)
logger = logging.getLogger(__name__)
logger.info("Логирование настроено")

# Валидация путей, указанных в файле конфига
try:
    validate_paths(PATHS_TO_VALIDATE, create_missing_dirs=CREATE_MISSING_DIRS)
    logger.info("Пути провалидированы")
    validate_config()
    logger.info("Конфиг провалидирован")
except PathValidationError as e:
    logger.critical(f"Проверьте необходимые для работы программы директории и файлы: {e}")
    raise SystemExit(1)


if __name__ == "__main__":
    try:
        # Инициализация БД и таблицы
        init_db()
        # Чтение данных из файла
        json_data = read_input_data(INPUT_FILE_PATH)
        # Форматирование данных
        formatted_data, rows_cnt = format_and_deduplicate_data(json_data)
        # Запись данных в таблицу
        insert_data(formatted_data, rows_cnt)
    except Exception as e:
        logger.error(e)
