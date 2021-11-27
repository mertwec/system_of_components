# from decimal import Decimal


# for pattern
def check_exist_value_in_db(new_value, values_in_db):
    """ for creating new element in DB, if it exists in BD
    return True, else False
    :param new_value: str or tuple of strs
    :param values_in_db: generator of values or tuples
    :return: bool
    """
    return new_value in values_in_db


def _category_unit(unit, category) -> bool:
    """
    checking if the "unit" parameter matches the "category"
    :param unit:
    :param category:
    :return: True if crash validation
    """
    check = {'R': 'resistor',
             'F': 'capacitor',
             'z': 'quartz',
             'H': 'inductance', }
    if unit == "None" and category in check.values():
        print(1)
        return True
    elif unit[-1] == 'R' and category != check['R']:
        print(2)
        return True
    elif unit[-1] == 'F' and category != check['F']:
        print(3)
        return True
    elif unit[-1] == 'H' and category != check['H']:
        print(4)
        return True
    elif unit[-1] == 'z' and category != check['z']:
        print(5)
        return True
    else:
        return False


def generate_component_for_db(data: dict) -> dict or str:
    """conversion form to dictionary for database
    :param data: dict from form "component"
    :return: str if error of validations
            dict if all rights
    """
    if _category_unit(data['unit'], data['category']):
        return 'unit and category do not correspond!'

    if data['unit'] != "None":
        value = f"{data['value'].upper()}{data['unit']}"
    else:
        value = data['value'].upper()

    del data["csrf_token"]
    del data['submit']
    up_data = {"value": value,
               "power": float(data['power']),
               "category_name": data['category'],
               "pattern_name": data['pattern'],
               }
    data.update(up_data)
    return data
