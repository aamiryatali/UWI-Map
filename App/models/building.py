from App.database import db

class Building(db.Model):
    buildingID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    markers = db.relationship('Marker', backref='buildingID', lazy=True)

    def __init__(self, name):
       self.name = name

    def getMarkers(self):
        return self.markers