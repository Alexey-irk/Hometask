import csv
import os

import openpyxl
import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла. Возвращает список словарей с транзакциями."""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except Exception as ex:
        print(f"Ошибка при чтении: {ex}")
        return []


def read_transactions_xlsx(file_path: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла (.xlsx).Возвращает список словарей с транзакциями."""
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        return df.to_dict(orient="records")
    except Exception as ex:
        print(f"Ошибка при чтении: {ex}")
        return []


if __name__ == "__main__":
    print(read_transactions_csv("C:/Users/User/PycharmProjects/Hometask/data/transactions.csv"))
    print(read_transactions_xlsx("C:/Users/User/PycharmProjects/Hometask/data/transactions_excel.xlsx."))
