import json
import os


def load_transactions(file_path: str) -> list[dict]:
    """Загружает список транзакций из JSON-файла."""

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []


if __name__ == "__main__":
    print(load_transactions("C:/Users/User/PycharmProjects/Hometask/data/operations.json"))
