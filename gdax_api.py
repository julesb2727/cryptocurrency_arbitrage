import gdax
import numpy as np

public_client = gdax.PublicClient()

def get_gdax_prices(client):
    products = ["BTC-USD","BTC-EUR","ETH-USD","ETH-BTC","ETH-EUR","LTC-USD","LTC-BTC","LTC-EUR"]

    prices = {}
    for prod in products:
        tick = client.get_product_ticker(product_id=prod)
        prices[prod] = tick["price"]

    return prices

prices = get_gdax_prices(public_client)
print(prices)