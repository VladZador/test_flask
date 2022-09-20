import requests


def get_currency_exchange_rate(user_date: str,
                               user_currency: str,
                               user_bank: str):
    response = requests.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={user_date}")
    resp_json = response.json()

    if response.status_code == 200:
        exist_currencies = []
        for currencies_dict in resp_json["exchangeRate"]:
            if currencies_dict.get("currency") == user_currency:
                if user_bank == "NB":
                    sale_rate = currencies_dict.get("saleRateNB")
                    return f"NBU exchange rate on {user_date} when converting UAH " \
                           f"to {user_currency} - {sale_rate}"
                elif user_bank == "PB":
                    try:
                        sale_rate = currencies_dict["saleRate"]
                        purchase_rate = currencies_dict["purchaseRate"]
                        return f"PrivatBank exchange rate on {user_date} when converting UAH to {user_currency}: " \
                               f"sale rate - {sale_rate} and purchase rate - {purchase_rate}"
                    except KeyError:
                        return f"Sorry, there is no PrivatBank exchange rate for {user_currency} on {user_date}"
                else:
                    return f"Wrong bank code. Use NB for National Bank of Ukraine or PB for PrivatBank."
            else:
                if currencies_dict.get("currency"):
                    exist_currencies.append(currencies_dict.get("currency"))
        else:
            if exist_currencies:
                currencies_info = "Available currencies are: " + ", ".join(exist_currencies)
            else:
                currencies_info = ""
            return f"There is no exchange rate UAH to {user_currency} on {user_date}. " + currencies_info
    else:
        return f"Api error {response.status_code}: {resp_json.get('errorDescription')}"


if __name__ == "__main__":
    print(get_currency_exchange_rate("15.07.2020", "PLN", "NB"))
