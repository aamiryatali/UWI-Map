from App.database import db
from .marker import Marker

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    drawingCoords = db.Column(db.JSON)
    markers = db.relationship('Marker', backref='building')
    facultyID = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    image = db.Column(db.String(200), nullable=True, default='')

    def __init__(self, name, facultyID, drawingCoords):
        self.name = name
        self.facultyID = facultyID
        self.drawingCoords = drawingCoords

    def addImage(self, image):
        self.image = image
        db.session.add(self)
        db.session.commit()
        
    def getMarkers(self):
        return self.markers
    
    def addDrawing(self, drawingCoords):
        self.drawingCoords = drawingCoords
        db.session.add(self)
        db.session.commit()

    def addMarker(self, x, y, name, floor, description=None):
        marker = Marker.query.filter_by(name=name).first()
        if marker:
            if marker not in self.markers:
                self.markers.append(marker)
                db.session.add(self)
                db.session.commit()
                return marker
            else:
                return False
  
        marker = Marker(x, y, name, floor, self.id, description)
        if not marker:
            db.session.rollback()
            return False

        self.markers.append(marker)
        db.session.add(marker)
        db.session.commit()
        return marker