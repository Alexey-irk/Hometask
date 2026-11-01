import json
import re
from collections import Counter
from typing import Any


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_operations: list[dict[str, Any]] = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)

    return filtered_operations


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по значению ключа 'date'"""
    return sorted(operations, key=lambda operation: operation.get("date", ""), reverse=reverse)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует список банковских операций по строке поиска в описании."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = [
        operation for operation in data if "description" in operation and pattern.search(operation["description"])
    ]

    return filtered_data


file_path = "C:/Users/User/PycharmProjects/Hometask/data/operations.json"
search_query = "Перевод"  # input()

with open(file_path, "r", encoding="utf-8") as file:
    operations_list = json.load(file)

result = process_bank_search(operations_list, search_query)

print(result)


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Принимает список операций и список категорий.
    Возвращает словарь с количеством операций для каждой из указанных категорий.
    В расчет берутся названия категорий из поля 'description'."""
    all_descriptions = [transaction["description"] for transaction in data if "description" in transaction]

    counts = Counter(all_descriptions)

    # Формируем итоговый словарь только для запрошенных категорий
    return {category: counts[category] for category in categories}
