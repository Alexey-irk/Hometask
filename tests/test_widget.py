from src.widget import mask_account_card, get_date
from pytest import mark


def test_mask_account_card():
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


@mark.parametrize("number, expected", (("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
                                       ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
                                       ("Счет 35383033474447895560", "Счет **5560")))
def test_mask_account_card_parametrize(number, expected):
    assert mask_account_card(number) == expected
