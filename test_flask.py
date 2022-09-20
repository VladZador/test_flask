from flask import Flask, request

from utils import get_currency_exchange_rate

app = Flask(__name__)


@app.route("/")
def hello_world():
    return"<p>Hello, World!</p>"


@app.route("/rates", methods=["GET"])
def get_rates():
    date = request.args.get("date", default="01.12.2014")

    """Since PB provides exchange rate API only for UAH, the default base currency is UAH
    The "currency" variable corresponds to the conversion currency"""
    currency = request.args.get("currency", default="USD")
    bank = request.args.get("bank", default="NB")
    result = get_currency_exchange_rate(date, currency, bank)
    return result
