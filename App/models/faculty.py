from App.database import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    abbr = db.Column(db.String(50))
    buildings = db.relationship('Building', backref='faculty', lazy=True)

    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

    def getBuildings(self):
            return self.buildings
    
    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'abbr' : self.abbr,
            'buildings' : [building.to_dict() for building in self.buildings]
        }