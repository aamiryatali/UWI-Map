from App.database import db

class Faculty(db.Model):
    facultyName = db.Column(db.String(20), primary_key=True)
    buildings = db.relationship('Building', backref='facultyName', lazy=True)
    markers = db.relationship('Marker', backref='building', lazy=True)

    def __init__(self, facultyName):
        self.facultyName = facultyName

    def getBuildings(self):
            return self.buildings