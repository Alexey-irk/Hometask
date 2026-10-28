from unittest.mock import Mock, patch

import pandas as pd

from src.finance.reader import read_transactions_csv, read_transactions_xlsx


def test_read_transactions_csv_empty_file():
    mock_df = pd.DataFrame()
    with patch("src.finance.reader.pd.read_csv") as mock_read_csv:
        mock_read_csv.return_value = mock_df
        result = read_transactions_csv("empty.csv")

        assert result == []


def test_read_transactions_xlsx_empty_file():
    mock_df = pd.DataFrame()
    with patch("src.finance.reader.pd.read_excel") as mock_read_excel:
        mock_read_excel.return_value = mock_df
        result = read_transactions_xlsx("empty_excel.xlsx")

        assert result == []


def test_read_transactions_xlsx_success():
    mock_df = pd.DataFrame([{"id": 101, "amount": 5000.0}])

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = mock_df

        result = read_transactions_xlsx("fake_excel.xlsx")

        assert result == ([{"id": 101, "amount": 5000.0}])

        mock_read_excel.assert_called_once_with("fake_excel.xlsx", engine="openpyxl")


def test_read_transactions_csv_success():
    mock_df = pd.DataFrame([
        {"id": 1, "amount": 100.0},
        {"id": 2, "amount": -50.5}
    ])

    with patch("src.finance.reader.pd.read_csv") as mock_read_csv:
        mock_read_csv.return_value = mock_df

        result = read_transactions_csv("fake_path.csv")

        assert result == [
            {"id": 1, "amount": 100.0},
            {"id": 2, "amount": -50.5}
        ]
        mock_read_csv.assert_called_once_with("fake_path.csv")


def test_read_transactions_xlsx_error():
    with patch("src.finance.reader.pd.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = ValueError("Excel file format cannot be determined")
        result = read_transactions_xlsx("corrupted.xlsx")

        assert result == []

