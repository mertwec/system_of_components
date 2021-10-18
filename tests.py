import sys
from app_comp import db
from app_comp.models import temp_bd, Category, Pattern
from app_comp.tools import database_tools as dt
from app_comp.forms import existing_patterns, existing_categories




if __name__ == '__main__':
    patt = dt.read_from_table(db, Pattern)
    lp = [i.name for i in patt]
    print(existing_categories, existing_patterns)
    # for i in patt:
    #     print(type(i.name))

