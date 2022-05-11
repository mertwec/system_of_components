import json
import random
import os.path
from app_comp import path_to_json


# path_to_json = r"app_comp\static\quotes.json"


def get_json_data(path_):
    with open(path_, 'r') as json_object:
        json_data = json.load(json_object)
    return json_data


def add_quote_to_json(quote: str, author: str, path=path_to_json):
    data = get_json_data(path)
    data.append([quote, author])
    json_data = json.dumps(data)
    with open(path, "w") as quotes:
        quotes.write(json_data)
    print('complete')


def random_quote(path=path_to_json):
    quotes = get_json_data(path)
    return random.choice(quotes)


if __name__ == '__main__':
    path_to_json = r"..\static\quotes.json"
    print(random_quote(path=path_to_json))
