import requests
import os
from dotenv import load_dotenv

load_dotenv()


URL = "https://apilayer.com/exchangerates_data-api"
API_KEY = os.getenv("API_KEY")
headers = {"apikey": API_KEY}


def get_summ_transaction(transaction: dict) -> float:
    """Принимает на вход транзакцию и возвращает сумму транзакции"""
    payload = {
        "amount": transaction["operationAmount"]["amount"],
        "from": transaction["operationAmount"]["currency"]["code"],
        "to": "RUB",
    }
    if (
        transaction["operationAmount"]["currency"]["code"] == "USD"
        or transaction["operationAmount"]["currency"]["code"] == "EUR"
    ):
        try:
            response = requests.get(URL, headers=headers, params=payload)
            response.raise_for_status()
            response_json = response.json()
            if response_json.get("success", True):
                result = float(response_json.get("result"))
                return result
        except requests.exceptions.HTTPError:
            print("HTTP Error. Please check the URL.")
        except requests.exceptions.RequestException:
            print("An error occurred. Please try again later.")
        except Exception as ex:
            print(f"Возникла непридвиденная ошибка {ex}")
    return transaction["operationAmount"]["amount"]
