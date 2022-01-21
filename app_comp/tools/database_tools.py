from app_comp.models import Category, Pattern, Component, PCBoard
from app_comp import db


unit_list = [None, "R", "kR", "MR", "pF", "mkF", 'mkH', 'kHz', "MHz"]


class CRUDTable:
    def __init__(self):
        self.db = db

    def read_table_all(self, table: object):  # Category or Category.name
        """read all information from the table
        :type
        """
        return self.db.session.query(table).all()

    def read_table_first(self, table: object):  # Category or Category.name
        """read all information from the table
        :type
        """
        return self.db.session.query(table).first()

    def write_to_table_column(self, column: object):
        """
        :param column: new object for writing in table
        example: column = Column(arg1=arg1, arg2=arg2, ... argN=argN)
        """
        self.db.session.add(column)
        self.db.session.commit()

    def read_table_filter_first(self, table, filter_param: tuple) -> list:
        """
        :param table: name of table: Component, PCBoard, etc/
        :param filter_param: tuple of filters: (Component.name=='name', table.id=n, ets)
        :return: result search: [], if nothing
        """
        return self.db.session.query(table).filter(*filter_param).first()

    def read_table_filter(self, table, filter_param: tuple) -> list:
        """
        :param table: name of table: Component, PCBoard, etc/
        :param filter_param: tuple of filters: (Component.name=='name', table.id=n, ets)
        :return: result search: [], if nothing
        """
        return self.db.session.query(table).filter(*filter_param).all()

    def read_table_sorted(self, table, sorted_param):
        return self.db.session.query(table).order_by(sorted_param).all()

    def delete_table_column(self, column: object):
        """
        :param column: column for dell
        example: object from table: column = db.session.query(Column in table)
        :return: None
        """
        self.db.session.delete(column)
        self.db.session.commit()


crud = CRUDTable()
existing_patterns = [p[0] for p in crud.read_table_all(Pattern.name)]
existing_categories = [c[0] for c in crud.read_table_all(Category.name)]


def create_category(name, refdes):
    cat = Category(name=name, refdes=refdes)
    crud.write_to_table_column(cat)


def map_refdes_category() -> dict:
    """
    :return: dict(refdes: category name)
    """
    return {i.refdes: i.name for i in crud.read_table_all(Category)}


def create_component(kwarg: dict):
    """ write only in table "Component"
    :param kwarg: dict of parameters component
    :return: None
    """
    # print(kwarg)
    component = Component(value=kwarg['value'],
                          tolerance=kwarg['tolerance'],
                          voltage=kwarg["voltage"],
                          power=kwarg["power"],
                          count=kwarg["count"],
                          comment=kwarg["comment"],
                          category_name=kwarg["category_name"],
                          pattern_name=kwarg["pattern_name"],)
    crud.write_to_table_column(component)


def get_components_from_category(category, *args):
    filter_param = Component.category_name == category
    cat_components = db.session.query(*args).filter(filter_param).all()
    return cat_components


def search_component_in_db(component_param: dict) -> dict:
    """
    :param component_param: {value': out_value['value'],
                            'tolerance': out_value['tolerance'],
                            'voltage': out_value['voltage'],
                            'power': out_value['power'],
                            'comment': out_value['comment'],
                            'count': define_count(params_comp_pcb['Count']),
                            'pattern_name': define_pattern(params_comp_pcb['PatternName'], category),
                            'category_name': category}
    :return:  {value': out_value['value'],
                'tolerance': out_value['tolerance'],
                'voltage': out_value['voltage'],
                'power': out_value['power'],
                'comment': out_value['comment'],
                'count': define_count(params_comp_pcb['Count']),
                'pattern_name': define_pattern(params_comp_pcb['PatternName'], category),
                'category_name': category}
                +
                'id_component':((first id in db,))
    """
    cp = component_param
    if cp['category_name'] == 'resistor':
        _filter = (Component.value == cp['value'],
                   Component.pattern_name == cp['pattern_name'],
                   Component.tolerance == float(cp["tolerance"][:-1]))
    else:
        _filter = (Component.value == cp['value'],
                   Component.pattern_name == cp['pattern_name'])
    cp['id_component'] = crud.read_table_filter_first(Component.id, _filter)
    return cp


def exists_components_in_db(pcb_components: list) -> tuple:
    """
    :param pcb_components:
    :return: ([existing_pcb_components_in_db],[not_existing_pcb_components_in_db])
    """
    pcb_components_in_db = list(map(search_component_in_db, pcb_components))
    existing_pcb_components_in_db = [i for i in pcb_components_in_db if i['id_component']]
    not_existing_pcb_components_in_db = [i for i in pcb_components_in_db if not i['id_component']]
    return existing_pcb_components_in_db, not_existing_pcb_components_in_db
