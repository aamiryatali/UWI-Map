from .user import create_user 
from .building import create_building
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    building = create_building("test")
    building.addDrawing('{"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[-61.400468, 10.642405], [-61.400468, 10.644958], [-61.396264, 10.644958], [-61.396264, 10.642405], [-61.400468, 10.642405]]]}}')
