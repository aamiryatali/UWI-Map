from .user import create_user 
from .building import create_building
from .faculty import create_faculty
from App.database import db
import json

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    #building = create_building("test", 1, '{"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[-61.400468, 10.642405], [-61.400468, 10.644958], [-61.396264, 10.644958], [-61.396264, 10.642405], [-61.400468, 10.642405]]]}}')
    eng = create_faculty('Faculty of Engineering', "ENG")
    fst = create_faculty('Faculty of Science & Technology', "FST")
    fhe = create_faculty('Faculty of Humanities & Education', "FHE")
    fol = create_faculty('Faculty of Law', "FOL")
    ffa = create_faculty('Faculty of Food & Agriculture', "FFA")
    fss = create_faculty('Faculty of Social Sciences', "FSS")
    fms = create_faculty('Faculty of Medical Sciences', "FMS")
    fsp = create_faculty('Faculty of Sport', "FSP")
    admin = create_faculty('Administrative & Student Services, Guild', "Admin/Guild")
    other = create_faculty('Institutes, Centers, Services, Recreation, Halls etc', "Other")
    