from masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """ Принимает строку с типом и номером карты или счёта,
    возвращает строку с замаскированным номером. """

    # Разделяем строку на части: тип (может состоять из нескольких слов) и номер
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

# def get_date_fast(date_str: str) -> str:
#     """Функция, которая принимает на вход строку с датой в формате
#     "2024-03-11T02:26:18.671407"  и возвращает строку с датой в формате
#     "ДД.ММ.ГГГГ" ("11.03.2024")."""
#     # Вырезаем "2024-03-11"
#     year, month, day = date_str[:10].split("-")
#     # Собираем в нужном порядке
#     return f"{day}.{month}.{year}"

from datetime import datetime


def get_date(date_str: str) -> str:
        # Превращаем строку в объект datetime
        dt = datetime.fromisoformat(date_str)
        # Форматируем в нужный вид: ДД.ММ.ГГГГ
        return dt.strftime("%d.%m.%Y")

    # Пример использования:
input_str = "2024-03-11T02:26:18.671407"
print(get_date(input_str))  # 11.03.2024
