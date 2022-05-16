from app_comp import db
from app_comp.tools.quotes import random_quote
# from app_comp.tools import database_tools as dbt

temp_bd = {'company': "Adeptus Mechanicus",
           'user': "Master Inquisitor",
           'contacts': "Mars. Valleys of the Mariner. F.'DevMechanic', s.42 r.3",
           # 'quote': random_quote(),     # type of "quote:list"=[quote:str, author:str]
           }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    refdes = db.Column(db.String(15), nullable=False)
    components = db.relationship('Component', backref='category',
                                 # lazy='joined',
                                 cascade='all, delete',)

    def __str__(self):
        return f'{self.id}: {self.refdes} - {self.name}'


class Pattern(db.Model):
    __tablename__ = 'patterns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    component = db.relationship('Component', backref='pattern',
                                # lazy='joined',
                                cascade='all, delete', passive_deletes=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

    def get_components_from_pattern(self):
        return [compt.get_parameters_as_dict() for compt in self.component]


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
    tolerance = db.Column(db.Float, default=None)   # %
    voltage = db.Column(db.Integer, default=None)  # V
    power = db.Column(db.Float, default=None)   # W
    count = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text)
    category_name = db.Column(db.String(128), db.ForeignKey("categories.name"))
    pattern_name = db.Column(db.String(128), db.ForeignKey("patterns.name"))

    pcboards = db.relationship("AssociatedCompPcb",
                               back_populates='component')

    def __str__(self):
        return f'Component: {self.value} tol: {self.tolerance}%\nPattern: {self.pattern_name}\nCount: {self.count}'

    def get_parameters_as_dict(self) -> dict:
        return {"category": self.category_name,
                "value": self.value,
                "tol, %": self.tolerance,
                "pattern": self.pattern_name,
                "voltage, V": self.voltage,
                "power, W": self.power,
                "commentary": self.comment,
                "count": self.count
                }


class PCBoard(db.Model):
    """Project for assembling printed circuit boards"""
    __tablename__ = 'PCB'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.Float, default=0.0)
    count_boards = db.Column(db.Integer, default=1)
    comment = db.Column(db.Text)
    components = db.relationship("AssociatedCompPcb",
                                 back_populates='pcb',
                                 cascade='all, delete')

    def __str__(self):
        return f"{self.name}-v{self.version}."

    def get_parameters_as_dict(self):
        _components = [(c.component, c.comp_count) for c in self.components]
        return {'name': f'{self.name}-v{self.version}',
                'comment': self.comment,
                'count_collect': self.count_boards,
                'components': _components,
                }
