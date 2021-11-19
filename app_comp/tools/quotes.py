import json
import random


path_to_json = "app_comp/static/quotes.json"


def get_json_data(path=path_to_json):
    with open(path, 'r') as json_object:
        json_data = json.load(json_object)
    return json_data


def add_quote_to_json(quote: str, author: str, path=path_to_json):
    data = get_json_data()
    data.append([quote, author])
    json_data = json.dumps(data)
    with open(path, "w") as quotes:
        quotes.write(json_data)
    print('complete')


def random_quote(quotes=get_json_data()):
    return random.choice(quotes)


if __name__ == '__main__':
    print(random_quote())
