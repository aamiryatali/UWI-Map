from App.models import Building
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_building(name, facultyID, drawingCoords):
    newBuilding = Building(name=name, facultyID=facultyID, drawingCoords=drawingCoords)
    try:
        db.session.add(newBuilding)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return False
    except Exception as e:
        db.session.rollback()
        return False
    return newBuilding

def get_building(name):
    building = Building.query.filter_by(name=name).first()
    if not building:
        return False
    return building
