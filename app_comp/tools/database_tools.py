from app_comp.models import Category, Pattern, Component, PCBoard, AssociatedCompPcb
from app_comp import db
from sqlalchemy.exc import ProgrammingError


unit_list = [None, "R", "kR", "MR", "pF", "mkF", 'mkH', 'kHz', "MHz"]


class CRUDTable:
    def __init__(self, database=db):
        self.db = database

    def read_element_on_id(self, table, id_elem):
        return self.db.session.query(table).get(id_elem)

    def read_table_all(self, table: object):  # Category or Category.name
        """read all information from the table
        :type
        """
        try:
            return self.db.session.query(table).all()
        except ProgrammingError:
            return list()

    def read_table_first(self, table: object):  # Category or Category.name
        """read all information from the table
        :type
        """
        return self.db.session.query(table).first()

    def read_table_id(self, table: object) -> int:  # Category
        return self.db.session.query(table.id).all()

    def write_to_table_column(self, column: object):
        """ param column: new object for writing in table
        example: column = Column(arg1=arg1, arg2=arg2, ... argN=argN)
        """
        self.db.session.add(column)
        self.db.session.commit()

    def write_n_column_to_table(self, columns: list):
        """ :param columns: list of new objects for writing in table
        :example: columns = [Column(arg1=arg1, arg2=arg2, ... argN=argN),
                            Column(arg1=arg1,.....), ... ]
        """
        self.db.session.add_all(columns)
        self.db.session.commit()

    def write_commit(self):
        self.db.session.commit()

    def read_table_filter_first(self, table, filter_param: tuple) -> list:
        """:param table: name of table: Component, PCBoard, etc/
        :param filter_param: tuple of filters: (Component.name=='name', table.id=n, ets)
        :return: result search: [], if nothing
        """
        if isinstance(table, (tuple, list)):
            return self.db.session.query(*table).filter(*filter_param).first()
        return self.db.session.query(table).filter(*filter_param).first()

    def read_table_filter(self, table, filter_param: tuple) -> list:
        """
        :param table: name of table -- Component, PCBoard, etc/
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
    print(kwarg)
    component = Component(value=kwarg['value'],
                          tolerance=kwarg['tolerance'],
                          voltage=kwarg["voltage"],
                          power=float(kwarg["power"]),
                          count=kwarg["count"],
                          comment=kwarg["comment"],
                          category_name=kwarg["category"],
                          pattern_name=kwarg["pattern"],)
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
                'count': define_count(params_comp_pcb['Count']),  # count component 'value' in pcb
                'pattern_name': define_pattern(params_comp_pcb['PatternName'], category),
                'category_name': category,
                +
                'id_component':((first id in db,)) or None
                'count_on_storage': count components in storage or None
                }
    """
    cp = component_param
    if cp['category_name'] == 'resistor':
        _filter = (Component.value == cp['value'],
                   Component.pattern_name == cp['pattern_name'],
                   Component.tolerance == float(cp["tolerance"][:-1]))
    else:
        _filter = (Component.value == cp['value'],
                   Component.pattern_name == cp['pattern_name'])
    id_component = crud.read_table_filter_first((Component.id, Component.count), _filter)  # (id,)

    if id_component:
        cp['id_component'] = id_component[0]    # id = (id,)
        cp['count_on_storage'] = id_component[1]
    else:
        cp['id_component'] = id_component       # None
        cp['count_on_storage'] = id_component   # None
    return cp


def exists_components_in_db(pcb_components: list) -> tuple:
    """
    check existing components in DB and file-report, when create new PCB
    :param pcb_components: all components in added PCBoard
    :return: ([existing_pcb_components_in_db],[not_existing_pcb_components_in_db])
    check existing components in db
    """
    pcb_components_in_db = list(map(search_component_in_db, pcb_components))
    existing_pcb_components_in_db = [i for i in pcb_components_in_db if i['id_component']]
    not_existing_pcb_components_in_db = [i for i in pcb_components_in_db if not i['id_component']]
    return existing_pcb_components_in_db, not_existing_pcb_components_in_db


def search_text(type_table: str, text_search: str) -> list:
    """
    param: table = Pattern, PCBoard or Component
    param: text_search: text for search
    return list """
    text = f'%{text_search}%'
    if type_table == 'Pattern':
        patterns = db.session.query(Pattern).filter(Pattern.name.like(text)).all()
        return patterns
    elif type_table == 'Component':
        return db.session.query(Component).filter(Component.value.like(text)).all()
    elif type_table == 'PCBoard':
        return db.session.query(PCBoard).filter(PCBoard.name.like(text)).all()


def check_count_component_from_pcb(pcb_components: list, N: int):
    """pcb_components: [(<Component>, k), (<Compnent>, k)...etc] where k= count components on pcb
    N: number pcb for collect
    """
    list_true = [(c[0], c[1]*N) for c in pcb_components if c[0].count > c[1]*N]
    list_false = [(c[0], c[1]*N) for c in pcb_components if c[0].count < c[1]*N]
    list_delta = [(c[0], c[1]*N - c[0].count) for c in pcb_components if c[0].count < c[1]*N]
    return {'component_enough': list_true,
            'component_not_enough': list_false,
            'component_delta': list_delta}
