from src.external_api import get_summ_transaction
from unittest.mock import patch, Mock


@patch("requests.get")
def test_usd_returns_converted_value(mock_get):
    # 1. Готовим вход: транзакция на 100 USD
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }

    mock_response = Mock()
    mock_response.raise_for_status = Mock
    mock_response.json.return_value = {"success": True, "result": 9500.0}
    mock_get.return_value = mock_response

    result = get_summ_transaction(transaction)

    assert result == 9500.0
    assert isinstance(result, float)
