from app_comp.models import Category, Pattern, Component
from app_comp import db


unit_list = [None, "R", "kR", "MR", "pF", 'nF', "mkF", 'mkH', 'kHz', "MHz"]


def read_from_table(dbase, table):
    return dbase.session.query(table).all()


existing_patterns = [p.name for p in read_from_table(db, Pattern)]
existing_categories = [c.name for c in read_from_table(db, Category)]


def write_component_to_table(db, kwarg: dict):
    # print(kwarg)
    component = Component(value=kwarg['value'],
                          tolerance=kwarg['tolerance'],
                          voltage=kwarg["voltage"],
                          power=kwarg["power"],
                          count=kwarg["count"],
                          comment=kwarg["comment"],
                          category_name=kwarg["category_name"],
                          pattern_name=kwarg["pattern_name"],)
    db.session.add(component)
    db.session.commit()


def write_pattern_to_table(db, arg):
    db.session.add(Pattern(name=arg))
    db.session.commit()


def get_components_from_category(db, category, *args):
    cat_components = db.session.query(*args).filter(Component.category_name == category).all()
    return cat_components
