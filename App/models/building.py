from App.database import db

class Building(db.Model):
    buildingID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    drawingCoords = db.Column(db.String(1000))
    markers = db.relationship('Marker', backref='building')

    def __init__(self, name):
        self.name = name

    def getMarkers(self):
        return self.markers
    
    def addDrawing(self, drawingCoords):
        self.drawingCoords = drawingCoords
        db.session.add(self)
        db.session.commit()
