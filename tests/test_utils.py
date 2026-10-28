import json
from unittest.mock import Mock, mock_open, patch

from src.utils import load_transactions


@patch("os.path.exists", return_value=True)
def test_load_transactions(mock_exist):
    test = [
        {
            "id": 422035015,
            "state": "EXECUTED",
            "date": "2019-02-27T03:59:25.921176",
            "operationAmount": {"amount": "69311.35", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на счет",
            "from": "MasterCard 8847384717023026",
            "to": "Счет 85458008326755993377",
        },
        {
            "id": 917824439,
            "state": "EXECUTED",
            "date": "2019-07-18T12:27:13.355343",
            "operationAmount": {"amount": "82139.20", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Platinum 6942697754917688",
            "to": "МИР 2956603572573342",
        },
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(test))):
        result = load_transactions("111.json")
    assert result == test
    mock_exist.assert_called_once_with("111.json")
