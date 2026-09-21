def get_mask_card_number(card_number: int) -> str:
    """ Функция принимает на вход номер карты и возвращает ее маску."""
    card_str: str = str(card_number)

    if len(card_str) != 16:
        return "Некорректный номер карты"

    first_6: str = card_str[:6]  # "700079"
    last_4: str = card_str[-4:]  # "6361"
    result: str = f"{first_6[:4]} {first_6[4:6]}** **** {last_4}"

    return result


print(get_mask_card_number(7000792289606361))  # 7000 79** **** 6361


def get_mask_account(account_number: int) -> str:
    """ Функция принимает на вход номер счета и возвращает его маску."""
    account_str: str = str(account_number)

    if len(account_str) < 4:
        return "Некорректный номер счета"

    last_4: str = account_str[-4:]
    return f"**{last_4}"


print(get_mask_account(73654108430135874305))  # **4305
