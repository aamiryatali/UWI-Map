from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x =  db.Column(db.Double, nullable=False)
    y = db.Column(db.Double, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    image = db.Column(db.String(200), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    buildingID = db.Column(db.Integer, db.ForeignKey('building.buildingID'))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_json(self):
        return{
            'x': self.x,
            'y': self.y
        }
