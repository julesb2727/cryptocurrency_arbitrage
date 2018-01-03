import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import gdax



def add_pair(graph, cur1, cur2, cur1_to_cur2):
    graph[cur1][cur2] = cur1_to_cur2
    return graph


def add_pair_w_inverse(graph, cur1, cur2, cur1_to_cur2):
    graph[cur1][cur2] = cur1_to_cur2
    graph[cur2][cur1] = 1 / cur1_to_cur2
    return graph


def print_arb(graph, dict, cycles):
    ans = []

    for cycle in cycles:
        if (len(cycle) > 2):
            gain = 1
            path = ""
            start = cycle[0]
            cycle.append(start)

            for i in range(len(cycle) - 1):
                cur1 = int(cycle[i])
                cur2 = int(cycle[i + 1])
                gain = gain * graph[cur1][cur2]
                path += dict[cur1] + "->"

            gain = gain * graph[cur2][start]
            path += dict[start]

            ans.append((path, gain))

    return sorted(ans, key=lambda tup: tup[1], reverse=True)



def get_gdax_prices(client):
    products = ["BTC-USD","BTC-EUR","ETH-USD","ETH-BTC","ETH-EUR","LTC-USD","LTC-BTC","LTC-EUR"]

    prices = {}
    for prod in products:
        tick = client.get_product_ticker(product_id=prod)
        print(tick)
        if tick == None:
            print("error in getting prices")
            return None
        prices[prod] = tick['price']

    print("got prices")

    return prices


public_client = gdax.PublicClient()
prices = get_gdax_prices(public_client)


num_currencies = 5
graph = np.eye(num_currencies)
cur_dict = {"USD": 0, "EUR": 1, "BTC": 2, "ETH": 3, "LTC": 4}
code_dict = {0:"USD", 1:"EUR", 2:"BTC", 3:"ETH", 4:"LTC"}

for key in prices:

    cur1 = key[:3]
    cur2 = key[4:]

    add_pair_w_inverse(graph, cur_dict[cur1], cur_dict[cur2], float(prices[key]) )

G = nx.to_networkx_graph(graph, create_using=nx.DiGraph())
cycles = list(nx.simple_cycles(G))
ans = print_arb(graph, code_dict, cycles)

for i in range(3):
        print(ans[i])
