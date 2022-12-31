import requests
import json
from os.path import join, dirname
from dotenv import load_dotenv
from dotenv import dotenv_values

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

exchanges = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}

config = dotenv_values(".env")
class Converter:
    @staticmethod
    def get_price(base, amount, sym):
        base_key = exchanges[base.lower()]
        sym_key = exchanges[sym.lower()]
        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/{config['API_KEY']}/latest/{base_key}")
        resp = json.loads(r.content)
        new_price = resp['conversion_rates'][sym_key] * float(amount)
        return new_price
