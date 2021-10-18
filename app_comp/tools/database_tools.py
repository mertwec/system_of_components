

def read_from_table(dbase, table):
    return dbase.session.query(table).all()


def write_to_table(db, table):
    pass



