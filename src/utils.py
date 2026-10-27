import json
import os
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("C:/Users/User/PycharmProjects/Hometask/logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict]:
    logger.info("Вызвана функция 'load_transactions'")
    """Загружает список транзакций из JSON-файла."""

    if not os.path.exists(file_path):
        logger.error("Файл транзакций не найден")
        return []

    try:
        logger.info("Открытие файла с транзакциями")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return []


if __name__ == "__main__":
    print(load_transactions("C:/Users/User/PycharmProjects/Hometask/data/operations.json"))
