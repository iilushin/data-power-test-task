import sqlite3
import logging
from typing import List, Tuple, Any

from configs.config import *
from utils import render_sql_templates

logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Инициализация БД и таблицы TABLE_NAME
    """
    try:
        logger.info("Создание БД и таблицы {TABLE_NAME}")

        # Генерация запроса для создания бд и таблицы
        sql_create_table_query = render_sql_templates.render_sql_template(SQL_CREATE_TABLE_QUERY_PATH,
                                                                          columns=INIT_TABLE_COLUMNS,
                                                                          table_name=TABLE_NAME)
        logger.info(f"Запрос на создание таблицы:\n{sql_create_table_query}")

        # Создание подключения, курсора, выполнение запроса, закрытие подключения
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_create_table_query)
        conn.commit()
        logger.info(f"База {SQLITE_DB_PATH} готова, таблица {TABLE_NAME} инициализирована")
        conn.close()
    except sqlite3.OperationalError as e:
        logger.error(f"Ошибка инициализации базы: {SQLITE_DB_PATH}, завершение работы программы: {e}")
        raise SystemExit(1)


def insert_data(data: List[Tuple], rows_cnt: int) -> None:
    """
    Вставка кортежей данных в таблицу бд
    """

    if rows_cnt > 0:
        # Генерация запроса для вставки данных в таблицу
        sql_insert_query = render_sql_templates.render_sql_template(SQL_INSERT_DATA_QUERY_PATH,
                                                                          columns=INIT_TABLE_COLUMNS,
                                                                          table_name=TABLE_NAME)
        try:
            logger.info(f"Вставка данных в таблицу {TABLE_NAME}")
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()
            before = conn.total_changes
            cursor.executemany(sql_insert_query, data)
            conn.commit()
            after = conn.total_changes
            conn.close()
            logger.info(
                f"{'Вставка данных в таблицу ' + str(TABLE_NAME) + 'прошла успешно, количество вставленных строк: ' 
                   + str(after - before) if after - before != 0 else 'Ни одна строка не была вставлена в таблицу'}"
            )
        except sqlite3.OperationalError as e:
            logger.error(f"Ошибка при вставке данных в таблицу {TABLE_NAME}, завершение работы программы: {e}")
            raise SystemExit(1)
    else:
        logger.warning(f"Вставка данных в таблицу {TABLE_NAME} не была произведена, так как нет уникальных строк для вставки")


def get_data(get_type: str) -> List[Tuple]:
    """
    Получение данных из бд
    get_type: all_cols - select *, получение всех данных. dedup_cols - получение только колонок для дедупликации
    """

    if get_type == "all_cols":
        # Генерация запроса для получения всех данных из таблицы
        sql_select_query = render_sql_templates.render_sql_template(SQL_SELECT_DATA_QUERY_PATH,
                                                                    table_name=TABLE_NAME)
        logger.info(f"\nЗапрос на получение всех данных:\n{sql_select_query}")

    elif get_type == "dedup_cols":
        # Генерация запроса для получения части данных из таблицы
        sql_select_query = render_sql_templates.render_sql_template(SQL_SELECT_DEDUP_DATA_QUERY_PATH,
                                                                    table_name=TABLE_NAME,
                                                                    columns=DEDUPLICATE_DATA_BY_COLUMNS)
        logger.info(f"\nЗапрос на получение колонок {DEDUPLICATE_DATA_BY_COLUMNS}:\n{sql_select_query}")
    else:
        msg = "Некорректный параметр get_type, укажите параметр из списка: all_cols, dedup_cols"
        logger.error(msg)
        raise SystemExit(1)

    try:
        logger.info(f"Получение данных из таблицы {TABLE_NAME}")
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        conn.close()
        logger.info(f"Данные из таблицы {TABLE_NAME} получены, {len(rows)} строк")
        return rows
    except sqlite3.OperationalError as e:
        logger.error(f"Ошибка при получении данных из таблицы {TABLE_NAME}, завершение работы программы: {e}")
        raise SystemExit(1)
