from App.models import Marker
from App.database import db

def get_marker(name):
    marker = Marker.query.filter_by(name=name).first()
    if marker:
        return marker
    return False