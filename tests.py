import sys
from app_comp import db
from app_comp.models import temp_bd, \
                            Category, \
                            Pattern, \
                            Component, \
                            PCBoard, \
                            AssociatedCompPcb
from app_comp.tools import database_tools as dt
from app_comp.tools import forms_validation as fv
from app_comp.tools.database_tools import get_components_from_category, \
                                        write_column_to_table


def test_get_comps_from_cat(category, db=db):
    cfcat = get_components_from_category(db, category, Component)
    return cfcat


def test_add_comp_pcb():
    b1 = db.session.query(PCBoard).get(1)
    comp2 = db.session.query(Component).get(7)
    comp3 = db.session.query(Component).get(8)
    print(b1)
    print(comp2, '\n', comp3)
    ass1 = AssociatedCompPcb(comp_count=2, pcb_id=b1.id, comp_id=comp2.id)
    ass2 = AssociatedCompPcb(comp_count=2, pcb_id=b1.id, comp_id=comp3.id)
    db.session.add_all([ass1, ass2])
    print(db.session.new)
    db.session.commit()
    print('done')


def test_get_pcb():
    pcbs = db.session.query(PCBoard).get(1)
    print(pcbs)
    for i in pcbs.components:
        print(i.component.get_parameters_as_dict())


def test_get_pcb_from_comp():
    c = db.session.query(Component).get(5)
    print(c)
    print(c.pcboards)
    for i in c.pcboards:
        print(i.pcb)
        print(i.component)


if __name__ == '__main__':
    # test_add_comp_pcb()
    # test_get_pcb()
    dt.create_category(db, "connector", "X")
