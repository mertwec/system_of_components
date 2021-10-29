from app_comp import db


temp_bd = {'company': 'TorsionPLUS',
           "user": "Master",
           'Email': ""
           }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    refdes = db.Column(db.String(15), nullable=False)
    components = db.relationship('Component',
                                 backref='category',
                                 lazy=True,
                                 cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.id}: {self.refdes} - {self.name} '


class Pattern(db.Model):
    __tablename__ = 'patterns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    component = db.relationship('Component', backref='pattern',
                                cascade='all, delete-orphan', )

    def __str__(self):
        return f'{self.id}: {self.name}'


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), unique=True, index=True, nullable=False)
    tolerance = db.Column(db.Integer, default=None)   # %
    voltage = db.Column(db.Integer, default=None)  # V
    power = db.Column(db.Float, default=None)
    count = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text)
    category_name = db.Column(db.String(128), db.ForeignKey("categories.name"))
    pattern_name = db.Column(db.String(128), db.ForeignKey("patterns.name"))

    def __str__(self):
        return f'{self.value} {self.pattern_name}; count={self.count} id:({self.id})'


class PCBoard(db.Model):
    __tablename__ = 'PCB'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.String(32), default='v1.0')
