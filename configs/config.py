"""
Модуль для конфигурирования путей проекта
"""
import os

# Параметры запуска
WRITE_LOGS_INTO_FILE = True # Нужно ли писать логи в файл
CREATE_MISSING_DIRS = True # Нужно ли создавать недостающие для работы программы директории автоматически

# Логирование
LOGGING_CONFIG_PATH = "configs/logging.yaml" # Конфиг логов
LOGGING_DIR_PATH = "logs/" # Директория с логами
LOGGING_FILE_NAME = "etl_logs.log" # Имя файла логов
LOGGING_FILE_PATH = os.path.join(LOGGING_DIR_PATH, LOGGING_FILE_NAME) # Полный путь к файлу с логами

# Путь к данным
INPUT_DATA_PATH = "data/input_data/" # Входные данные
INPUT_FILE_NAME = "ozon_orders.json" # Имя файла с входными данными
INPUT_FILE_PATH = os.path.join(INPUT_DATA_PATH, INPUT_FILE_NAME)

OUTPUT_DATA_PATH = "data/output_data/" # Выходные данные
OUTPUT_FILE_NAME = "results.csv" # Имя файла с результатами
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DATA_PATH, OUTPUT_FILE_NAME)

# Путь к базе SQLite
SQLITE_DB_DIR_PATH = "db/" # Дирекория с бд SQLite3
SQLITE_DB_NAME = "sqlite.db" # Имя бд SQLite3
SQLITE_DB_PATH = os.path.join(SQLITE_DB_DIR_PATH, SQLITE_DB_NAME) # Полный путь к файлу бд SQLite3

# Параметры работы с таблицей
TABLE_NAME = "orders" # Имя таблицы
RECREATE_TABLE_EVERY_RUN = False # Надо ли пересоздавать таблицу с каждым новым запуском
INIT_TABLE_COLUMNS = {
            "order_id": {"data_type": "TEXT", "is_nullable": False, "is_PK": True},
            "status": {"data_type": "TEXT", "is_nullable": False, "is_PK": False},
            "date": {"data_type": "TIMESTAMP", "is_nullable": False, "is_PK": False},
            "amount": {"data_type": "REAL", "is_nullable": False, "is_PK": False},
            "customer_region": {"data_type": "TEXT", "is_nullable": True, "is_PK": False},
                } # Не поддерживаются составные PK
DEDUPLICATE_DATA_BY_COLUMNS = ("order_id",)  # Кортеж колонок, по которым нужно дедуплицировать данные.
                                           # Если кортеж пустой - дедупликация производиться не будет
                                           # Если в таблице есть PK - при вставке дубли по PK будут игнорироваться в любом случае

# Скрипты SQL, необходимые для работы
SQL_QUERIES_DIR_PATH = "sql_queries/"

SQL_CREATE_TABLE_QUERY_NAME = "init_table.sql" # Инициализация таблицы order
SQL_CREATE_TABLE_QUERY_PATH = os.path.join(SQL_QUERIES_DIR_PATH, SQL_CREATE_TABLE_QUERY_NAME)

SQL_INSERT_DATA_QUERY_NAME = "insert_data.sql" # Вставка данных в таблицу order
SQL_INSERT_DATA_QUERY_PATH = os.path.join(SQL_QUERIES_DIR_PATH, SQL_INSERT_DATA_QUERY_NAME)

SQL_SELECT_DATA_QUERY_NAME = "select_all_data.sql"
SQL_SELECT_DATA_QUERY_PATH = os.path.join(SQL_QUERIES_DIR_PATH, SQL_SELECT_DATA_QUERY_NAME)

SQL_SELECT_DEDUP_DATA_QUERY_NAME = "select_data_for_deduplication.sql"
SQL_SELECT_DEDUP_DATA_QUERY_PATH = os.path.join(SQL_QUERIES_DIR_PATH, SQL_SELECT_DEDUP_DATA_QUERY_NAME)

# Пути, которые необходимо валидировать перед запуском программы
PATHS_TO_VALIDATE = {
    "dirs": [
        LOGGING_DIR_PATH,
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        SQLITE_DB_DIR_PATH,
        SQL_QUERIES_DIR_PATH,
    ],
    "files": [
        LOGGING_CONFIG_PATH,
        INPUT_FILE_PATH,
        SQL_CREATE_TABLE_QUERY_PATH,
        SQL_INSERT_DATA_QUERY_PATH,
        SQL_SELECT_DATA_QUERY_PATH,
        SQL_SELECT_DEDUP_DATA_QUERY_PATH,
    ]
}
