import time

import tinydb.database
from tinydb import TinyDB, where

from API.product import get_all_product


def get_product_data(database: tinydb.database.TinyDB, date_: str):
    return database.get(where("date") == date_)


def organize_data(data: dict, database: tinydb.database.TinyDB, date_: str, for_historic=True):
    product_data = get_product_data(database, date_)

    if not for_historic:
        product_data = None

    data_exist = False
    if product_data:
        product_data = dict(product_data)
        product_list = list(product_data.keys())
        data_exist = True

    else:
        product_data = {"date": date_, "day": time.strftime("%A")}
        product_list = []

    for product_name, unity, quantity, price in zip(data.get("name"), data.get("unity"), data.get("quantity"),
                                                    data.get("price")):
        if product_name in product_list:
            tmp_data = product_data.get(product_name)

            if unity in tmp_data.get("unity"):
                unity_index = tmp_data["unity"].index(unity)
                tmp_data["quantity"][unity_index] += int(quantity)
                tmp_data["price"][unity_index] += float(price)

            else:
                tmp_data["unity"].append(unity)
                tmp_data["quantity"].append(int(quantity))
                tmp_data["price"].append(float(price))

            product_data[product_name] = tmp_data

        else:
            for product_ in get_all_product():
                if product_.name == product_name:
                    product_type = product_.type

            product_data.update({
                product_name: {
                    "type": product_type,
                    "unity": [unity],
                    "quantity": [int(quantity)],
                    "price": [float(price)]
                }
            })

            product_list.append(product_name)

    if for_historic:
        if not data_exist:
            database.insert(product_data)
        else:
            database.update(product_data, where("date") == date_)
    else:
        organize_data(data, database, date_, True)
        return product_data
