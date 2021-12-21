from app_comp.models import Category, Pattern, Component, PCBoard
from app_comp import db


unit_list = [None, "R", "kR", "MR", "pF", "mkF", 'mkH', 'kHz', "MHz"]


def read_from_table(dbase, table):
    """read all information from the table
    :type
    """
    return dbase.session.query(table).all()


existing_patterns = [p.name for p in read_from_table(db, Pattern)]
existing_categories = [c.name for c in read_from_table(db, Category)]


def write_column_to_table(db, column: object):
    """
    :param column: object for writing in table
    example: column = Column(arg1=arg1, arg2=arg2, ... argN=argN)"""
    db.session.add(column)
    db.session.commit()


def create_category(db, name, refdes):
    cat = Category(name=name, refdes=refdes)
    write_column_to_table(db, cat)


def map_refdes_category(db) -> dict:
    return {i.refdes: i.name for i in read_from_table(db, Category)}


def create_component(db, kwarg: dict):
    """ write only in table "Component"
    :param db:
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
    write_column_to_table(db, component)


def get_components_from_category(db, category, *args):
    filter_param = Component.category_name == category
    cat_components = db.session.query(*args).filter(filter_param).all()
    return cat_components
