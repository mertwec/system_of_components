from app_comp import db
from app_comp.tools.quotes import random_quote


temp_bd = {'company': "Adeptus Mechanicus",
           'user': "Master Inquisitor",
           'contacts': "Mars. Valleys of the Mariner. F.'DevMechanic', s.42 r.3",
           'quote': random_quote(),     # type of "quote:list"=[quote:str, author:str]
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


class AssociatedCompPcb(db.Model):
    __tablename__ = 'component_pcb'
    pcb_id = db.Column(db.Integer, db.ForeignKey('PCB.id'), primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('components.id'), primary_key=True)
    comp_count = db.Column(db.Integer)

    component = db.relationship('Component', back_populates='pcboards')
    pcb = db.relationship('PCBoard', back_populates='components')


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), index=True, nullable=False)
    tolerance = db.Column(db.Integer, default=None)   # %
    voltage = db.Column(db.Integer, default=None)  # V
    power = db.Column(db.Float, default=None)   # W
    count = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text)
    category_name = db.Column(db.String(128), db.ForeignKey("categories.name"))
    pattern_name = db.Column(db.String(128), db.ForeignKey("patterns.name"))
    pcboards = db.relationship("AssociatedCompPcb",
                               back_populates='component')

    def __init__(self, value, voltage, tolerance, comment, count, power, pattern_name, category_name):
        self.value = value
        self.tolerance = tolerance
        self.voltage = voltage
        self.comment = comment
        self.count = count
        self.power = power
        self.pattern_name = pattern_name
        self.category_name = category_name

    def __str__(self):
        return f'id_{self.id}: {self.value} pattern:{self.pattern_name}; count={self.count} '

    def get_parameters_as_dict(self) -> dict:
        return {"value": self.value,
                "tol, %": self.tolerance,
                "pattern": self.pattern_name,
                "voltage, V": self.voltage,
                "power, W": self.power,
                "commentary": self.comment,
                "Count": self.count
                }


class PCBoard(db.Model):
    __tablename__ = 'PCB'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.Float, default=1.0)
    count_boards = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text)

    components = db.relationship("AssociatedCompPcb",
                                 back_populates='pcb',
                                 cascade='all, delete')

    def __str__(self):
        return f"{self.name}-{self.version}: {self.comment}; board count = {self.count_boards}"
