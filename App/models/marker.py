from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x =  db.Column(db.Double, nullable=False)
    y = db.Column(db.Double, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(200), nullable=True, default='')
    floor = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    buildingID = db.Column(db.Integer, db.ForeignKey('building.id'))

    def __init__(self, x, y, name, floor, buildingID, description=None):
        self.x = x
        self.y = y
        self.name = name
        self.floor = floor
        self.buildingID = buildingID
        self.description = description

    def addImage(self, image):
        self.image = image
        db.session.add(self)
        db.session.commit()
        
    def get_json(self):
        return{
            'x': self.x,
            'y': self.y
        }
