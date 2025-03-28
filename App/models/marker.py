from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x =  db.Column(db.Double, nullable=False)
    y = db.Column(db.Double, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    image = db.Column(db.String(200), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)

    def __init__(self, x, y, name, floor):
        self.x = x
        self.y = y
        self.name = name
        self.image = "template"
        self.floor = floor

    def addImage(self, path):
        self.image = path
        db.session.add(self)
        db.session.commit()

    def addDescription(self, description):
        self.description = description
        db.session.add(self)
        db.session.commit()

    def get_json(self):
        return{
            'x': self.x,
            'y': self.y
        }
