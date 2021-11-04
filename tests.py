import sys
from app_comp import db
from app_comp.models import temp_bd, Category, Pattern, Component
from app_comp.tools import database_tools as dt
from app_comp.tools import forms_validation as fv


if __name__ == '__main__':
    patt = dt.read_from_table(db, Pattern)
    lp = [i.name for i in patt]

    # for i in patt:
    #     print(type(i.name))

