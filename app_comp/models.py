from app_comp import db


temp_bd = {'company': 'TorsionPLUS',
           "user": "Walentin",
           }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    unit = db.Column(db.String(25), default=None)

    def __str__(self):
        return f'-{self.id}-{self.title}'
