from App.models import Building
from App.database import db

def create_building(name, facultyID, drawingCoords):
    newBuilding = Building(name=name, facultyID=facultyID, drawingCoords=drawingCoords)
    db.session.add(newBuilding)
    db.session.commit()
    return newBuilding

def get_building(name):
    building = Building.query.filter_by(name=name).first()
    if not building:
        return False
    return building