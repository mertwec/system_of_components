from app_comp import db


temp_bd = {'company': 'TorsionPLUS',
           "user": "Walentin",
           }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    unit = db.Column(db.String(25), default=None)

    def __str__(self):
        return f'{self.id}: {self.name} ({self.unit})'


"""
class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, unique=True, index=True, nullable=False)
    unit = db.Column(db.String(25), default=None)   # ???
    count = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text)

    category = None
    pattern = None

    def __str__(self):
        if self.unit:
            return f'{self.value} {self.unit} {self.pattern}; count={self.count} id:({self.id})'
        else:
            return f'{self.value} {self.pattern}; count={self.count} id:({self.id})'
"""
