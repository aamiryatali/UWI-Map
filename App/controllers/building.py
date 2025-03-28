from App.models import Building
from App.database import db

def create_building(name):
    newBuilding = Building(name=name)
    db.session.add(newBuilding)
    db.session.commit()
    return newBuilding