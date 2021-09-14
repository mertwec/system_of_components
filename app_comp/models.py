from app_comp import db


temp_bd = {'company': 'TorsionPLUS',
           "user": "Walentin",
           }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    unit = db.Column(db.String(50), default=None)   # Om, C , R, Hz
    refdes = db.Column(db.String(15), nullable=False)
    components = db.relationship('Component',
                                 backref='category',
                                 lazy=True,
                                 cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.id}: {self.refdes} - {self.name} ({self.unit})'


class Pattern(db.Model):
    __tablename__ = 'patterns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    component = db.relationship('Component', backref='pattern')

    def __str__(self):
        return f'{self.id}: {self.name}'


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), unique=True, index=True, nullable=False)
    tolerance = db.Column(db.Float, default=None)   # %
    unit = db.Column(db.String(25), default=None)                 # C(n,mk,p); R(k, M); L ()
    count = db.Column(db.Integer, default=0)    
    comment = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    pattern_id = db.Column(db.Integer, db.ForeignKey("patterns.id"))

    def __str__(self):
        if self.unit:
            return f'{self.value} {self.unit} {self.tolerance}% {self.pattern}; count={self.count} id:({self.id})'
        else:
            return f'{self.value} {self.pattern}; count={self.count} id:({self.id})'
