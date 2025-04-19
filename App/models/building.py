from App.database import db
from .marker import Marker
from sqlalchemy.exc import IntegrityError

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    drawingCoords = db.Column(db.JSON)
    markers = db.relationship('Marker', backref='building')
    facultyID = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    image = db.Column(db.String(200), nullable=True, default='')

    def __init__(self, name, facultyID, drawingCoords, description=None):
        self.name = name
        self.facultyID = facultyID
        self.drawingCoords = drawingCoords
        self.description = description

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

        try:
            self.markers.append(marker)
            db.session.add(marker)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return False
        except Exception as e:
            db.session.rollback()
            return False
        return marker
    
    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'drawingCoords' : self.drawingCoords,
            'description' : self.description,
            'markers' : self.markers,
            'facultyID' : self.facultyID,
            'image' : self.image,
            'facultyName' : self.faculty.name,
            'facultyAbbr' : self.faculty.abbr,
            'markers': [marker.to_dict() for marker in self.markers]
        }