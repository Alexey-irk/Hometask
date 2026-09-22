from masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(account_card_info: str) -> str:
    """ Принимает строку с типом и номером карты или счёта,
    возвращает строку с замаскированным номером. """

    # Разделяем строку на части: тип (может состоять из слов) и номер
    parts = account_card_info.rsplit(maxsplit=1)

    if len(parts) != 2:
        return "Некорректные данные"

    name, number = parts

    if not number.isdigit():
        return "Некорректный номер"

    # Для счета используем маску счета, для карты — маску карты
    if name.lower() == "счет":
        masked = get_mask_account(int(number))
    else:
        masked = get_mask_card_number(int(number))

    return f"{name} {masked}"


print(mask_account_card("Visa Platinum 7000792289606361"))


def get_date(date_string: str) -> str:
    """Принимает строку в формате ISO и возвращает в формате ДД.ММ.ГГГГ."""
    dt = datetime.fromisoformat(date_string)

    return dt.strftime("%d.%m.%Y")


input_date = "2024-03-11T02:26:18.671407"
print(get_date(input_date))  # 11.03.2024
