import json
import os
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.main import format_date, format_payment_info, get_file_transactions, main


def test_format_date_correct():
    """Проверка корректного форматирования даты."""
    assert format_date("2019-12-08T22:46:21.935582") == "08.12.2019"


def test_format_date_invalid():
    """Проверка поведения при некорректном формате даты."""
    assert format_date("") == ""


def test_format_payment_info_account():
    """Проверка маскирования счета без использования декораторов на функции."""
    with patch("src.main.get_mask_account") as mock_mask_account:
        mock_mask_account.return_value = "**4321"
        result = format_payment_info("Счет 41421565395219882431")

        assert result == "Счет **4321"
        mock_mask_account.assert_called_once_with("41421565395219882431")


def test_format_payment_info_card():
    """Проверка маскирования карты без использования декораторов на функции."""
    with patch("src.main.get_mask_card_number") as mock_mask_card:
        mock_mask_card.return_value = "7771 27** **** 3727"
        result = format_payment_info("MasterCard 7771273939393727")

        assert result == "MasterCard 7771 27** **** 3727"
        mock_mask_card.assert_called_once_with("7771273939393727")


@patch("builtins.input")
@patch("builtins.print")
def test_main_invalid_menu_choice(mock_print, mock_input):
    """Тестирование ввода несуществующего пункта меню."""
    mock_input.return_value = "9"

    main()

    # Добавлен \n в начале строки, так как в коде main() написано print("\nПрограмма: Неверный выбор...")
    mock_print.assert_any_call("\nПрограмма: Неверный выбор пункта меню. Программа завершена.")


@patch("pandas.read_csv", side_effect=Exception("Ошибка чтения"))
def test_get_file_transactions_csv_error(mock_read_csv):
    """Возврат пустого списка при исключении во время чтения CSV."""
    assert get_file_transactions(2) == []


def test_format_date_exception():
    """Если формат строки не ISO (нет дефисов или Т), возвращается сама строка."""
    assert format_date("08.12.2019") == "08.12.2019"


def test_format_payment_info_account_value_error():
    """Крайний случай: строка начинается со 'счет', но не содержит номера."""
    assert format_payment_info("Счет") == "Счет"


def test_format_payment_info_card_value_error():
    """Крайний случай: пустая маскировка карты при ValueError."""
    with patch("src.main.get_mask_card_number", side_effect=ValueError):
        assert format_payment_info("MasterCard 1234") == "MasterCard 1234"


@patch("src.main.get_file_transactions")
@patch("src.main.filter_by_state")
@patch("src.main.sort_by_date")
@patch("src.main.process_bank_search")
@patch("builtins.input")
@patch("builtins.print")
def test_main_full_execution_flow(mock_print, mock_input, mock_search, mock_sort, mock_filter, mock_get_transactions):
    """Полная сквозная проверка main со всеми шагами фильтрации и вывода."""

    # 1. Готовим тестовые данные
    mock_data = [
        {
            "date": "2019-12-08T22:46:21.935582",
            "description": "Перевод организации",
            "from": "MasterCard 7111222233334444",
            "to": "Счет 55556666777788889999",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "руб.", "code": "RUB"}},
        }
    ]

    # Настраиваем цепочку вызовов функций обработки данных
    mock_get_transactions.return_value = mock_data
    mock_filter.return_value = mock_data
    mock_sort.return_value = mock_data
    mock_search.return_value = mock_data

    # 2. Имитируем последовательные ответы пользователя на input()
    mock_input.side_effect = [
        "1",  # Выберите пункт меню (JSON)
        "EXECUTED",  # Введите статус для фильтрации
        "да",  # Отсортировать операции по дате?
        "убыванию",  # По возрастанию или по убыванию?
        "да",  # Выводить только рублевые транзакции?
        "да",  # Отфильтровать по определенному слову?
        "Перевод",  # Пользователь (введите слово)
    ]

    # 3. Запуск функции
    main()

    # 4. Проверяем, что все вспомогательные функции были вызваны корректно
    mock_get_transactions.assert_called_once_with("1")
    mock_filter.assert_called_once_with(mock_data, "EXECUTED")
    mock_sort.assert_called_once_with(mock_data, reverse=True)
    mock_search.assert_called_once_with(mock_data, "Перевод")

    # Проверяем, что в финальном принте вывелось верное количество найденных операций
    mock_print.assert_any_call("Программа:\nВсего банковских операций в выборке: 1\n")
