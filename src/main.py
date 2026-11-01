import json
import os

import pandas as pd

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, process_bank_search, sort_by_date


def get_file_transactions(choice: str) -> list[dict]:
    """Считывает транзакции из выбранного файла в пакете data."""
    base_dir = "data"

    if choice == "1":
        file_path = os.path.join(base_dir, "operations.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    elif choice == "2":
        file_path = os.path.join(base_dir, "transactions.csv")
        try:
            # Чтение CSV (используем разделитель-точку с запятой, пустые ячейки заменяем на "")
            df = pd.read_csv(file_path, sep=";").fillna("")
            return df.to_dict(orient="records")
        except Exception as ex:
            return []

    elif choice == "3":
        file_path = os.path.join(base_dir, "transactions_exels.xlsx")
        try:
            df = pd.read_excel(file_path).fillna("")
            return df.to_dict(orient="records")
        except Exception as ex:
            return []

    return []


def format_date(date_str: str) -> str:
    """Форматирует строку даты из ISO формата '2019-12-08T...' в '08.12.2019'."""
    if not date_str or not isinstance(date_str, str):
        return ""
    try:
        date_part = date_str.split("T")
        year, month, day = date_part[0].split("-")
        return f"{day}.{month}.{year}"
    except Exception as ex:
        return date_str


def format_payment_info(info_str: str) -> str:
    """Маскирует номер карты или счета, используя функции из src.masks."""
    if not info_str or (isinstance(info_str, float) and pd.isna(info_str)):
        return ""

    info_str = str(info_str).strip()
    if not info_str:
        return ""

    if info_str.lower().startswith("счет"):
        try:
            name, number = info_str.split(maxsplit=1)
            return f"{name} {get_mask_account(number)}"  # функция из masks.py
        except ValueError:
            return info_str
    else:
        try:
            parts = info_str.split()
            number = parts[-1]
            name = " ".join(parts[:-1])
            return f"{name} {get_mask_card_number(number)}"  # функция из masks.py
        except ValueError:
            return info_str


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input("\nПользователь: ").strip()

    file_types = {
        "1": "JSON-файл",
        "2": "CSV-файл",
        "3": "XLSX-файл",
    }

    if file_choice in file_types:
        print(f"\nПрограмма: Для обработки выбран {file_types[file_choice]}.")
    else:
        print("\nПрограмма: Неверный выбор пункта меню. Программа завершена.")
        return

    # Загрузка данных из файлов пакета data
    transactions = get_file_transactions(file_choice)

    # 1. Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status_input = input("\nПользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            transactions = filter_by_state(transactions, status_input)
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 2. Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("\nПользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("\nПользователь: ").strip().lower()

        reverse = True if "убыван" in order_choice else False
        transactions = sort_by_date(transactions, reverse=reverse)

    # 3. Фильтрация валюты (Рубли)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    currency_choice = input("\nПользователь: ").strip().lower()

    if currency_choice == "да":
        # Универсальная фильтрация для структуры JSON (вложенной) и таблиц (плоской)
        transactions = [
            op
            for op in transactions
            if (
                isinstance(op.get("operationAmount"), dict)
                and op["operationAmount"].get("currency", {}).get("code") == "RUB"
            )
            or (isinstance(op.get("currency_code"), str) and op.get("currency_code") == "RUB")
        ]

    # 4. Фильтрация по слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice = input("\nПользователь: ").strip().lower()

    if search_choice == "да":
        search_word = input("\nПользователь (введите слово): ").strip()
        transactions = process_bank_search(transactions, search_word)

    # 5. Вывод результатов в консоль
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(transactions)}\n")

    for op in transactions:
        date = format_date(op.get("date", ""))
        description = op.get("description", "")

        from_info = format_payment_info(op.get("from", ""))
        to_info = format_payment_info(op.get("to", ""))

        if from_info:
            transfer_route = f"{from_info} -> {to_info}"
        else:
            transfer_route = to_info

        # Универсальное извлечение суммы и названия валюты
        amount_data = op.get("operationAmount", {})
        if isinstance(amount_data, dict):
            amount = amount_data.get("amount", "0")
            currency = amount_data.get("currency", {}).get("name", "")
        else:
            amount = op.get("amount", "0")
            currency = op.get("currency_name", "")

        print(f"{date} {description}")
        if transfer_route:
            print(transfer_route)
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
