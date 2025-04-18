from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x =  db.Column(db.Double, nullable=False)
    y = db.Column(db.Double, nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)
    image = db.Column(db.String(200), nullable=True, default='')
    floor = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
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

    def resetBuildingDefault(self):
        self.buildingID = 1
        db.session.add(self)
        db.session.commit()
        return True
    
    def to_dict(self):
        return {
            'id' : self.id,
            'x' : self.x,
            'y' : self.y,
            'name' : self.name,
            'floor' : self.floor,
            'buildingID' : self.buildingID,
            'image' : self.image,
            'description' : self.description,
            'buildingName' : self.building.name,
            'facultyName' : self.building.faculty.name,
            'facultyAbbr' : self.building.faculty.abbr
        }