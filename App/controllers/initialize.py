from .user import create_user
from .building import create_building
from .faculty import create_faculty
from App.database import db
import json

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    building = create_building("N/A", 10, '{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-61.57974,10.638609],[-61.57974,10.63901],[-61.579182,10.63901],[-61.579182,10.638609],[-61.57974,10.638609]]]}}')
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
    