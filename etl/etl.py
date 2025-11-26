"""
Модуль для чтения и преобразования данных
"""

import json
import logging
from typing import List, Dict, Tuple

from configs.config import INPUT_FILE_NAME, DEDUPLICATE_DATA_BY_COLUMNS, INIT_TABLE_COLUMNS
from db.db import get_data

logger = logging.getLogger(__name__)

def read_input_data(path_to_data: str, file_name: str =INPUT_FILE_NAME) -> List[Dict] | None:
    """
    Функция для чтения входного файла
    """
    logger.info(f"Чтение входного файла {file_name}")
    try:
        with open(path_to_data) as json_file:
            data = json.load(json_file)
            logger.info(f"Данные из файла {file_name} успешно прочитаны, {len(data)} строк")
            return data
    except Exception as e:
        logger.error(f"Ошибка при чтении входного файла: {e}, завершение работы программы")
        raise SystemExit(1)


def deduplicate_by_columns(formatted_data: List[Tuple]) -> Tuple[List, List]:
    """
    Функция для дедупликации данных по списку DEDUPLICATE_DATA_BY_COLUMNS из конфига
    """

    logger.info(f"Будет произведено дедуплицирование по следующим полям: {", ".join(DEDUPLICATE_DATA_BY_COLUMNS)}")

    # Получение существующих колонок в таблице
    result_data = get_data(get_type="dedup_cols")

    seen = set(result_data)
    unique_rows = []
    duplicates = []

    for row in formatted_data:
        key = tuple(row[col] for col in DEDUPLICATE_DATA_BY_COLUMNS)
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)
            unique_rows.append(row)

    logger.info(f"Найдено {len(duplicates)} дубликатов, будет произведена вставка {len(unique_rows)} строк")

    return unique_rows, duplicates


def format_and_deduplicate_data(json_data: List[Dict]) -> Tuple[List[Tuple], int | None]:
    """
    Функция для форматирования и дедупликации данных. Приводит дату к нужному виду и возвращает список кортежей
    """
    result_list = []

    try:
        logger.info("Форматирование прочитанных файлов и подготовка их к вставке в БД")
        for order in json_data:
            result_list.append({"order_id": order["order_id"],
                                "status": order["status"],
                                "date": order["date"].replace("T", " "),
                                "amount": order["amount"],
                                "customer_region": order["customer"]["region"]})
        logger.info("Данные успешно отформатированы")
    except Exception as e:
        logger.error(f"Ошибка при форматировании данных: {e}")
        raise SystemExit(1)

    if DEDUPLICATE_DATA_BY_COLUMNS:
        unique_rows, duplicates = deduplicate_by_columns(result_list)
        return [tuple(d.values()) for d in unique_rows], len(unique_rows)

    return [tuple(d.values()) for d in result_list], None

