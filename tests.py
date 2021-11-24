import sys
from app_comp import db
from app_comp.models import temp_bd, Category, Pattern, Component
from app_comp.tools import database_tools as dt
from app_comp.tools import forms_validation as fv

'u101trans - v3.0-6kW'
if __name__ == '__main__':
    patt = dt.read_from_table(db, Pattern)
    lp = [i.name for i in patt]
    print(lp)
    for i in patt:
        print(type(i.name))

