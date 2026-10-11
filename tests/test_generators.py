from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from pytest import mark


def test_filter_by_currency_usd(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)

    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)
    assert [t["id"] for t in result] == [939719570, 142264268]


@mark.parametrize("currency, expected_ids", (("USD", [939719570, 142264268]),
                                             ("RUB", [873106923])))

def test_filter_by_currency(transactions, currency, expected_ids):
    result = list(filter_by_currency(transactions, currency))
    result_ids = [t["id"] for t in result]

    assert result_ids == expected_ids


def test_five_cards_from_one():
        result = list(card_number_generator(1, 5))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]


def test_empty_list_returns_empty_iterator():
    result = list(transaction_descriptions([]))
    assert result == []