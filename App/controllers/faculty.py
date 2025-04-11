from App.models import Faculty
from App.database import db

def create_faculty(name, abbr):
    newFaculty = Faculty(name=name, abbr=abbr)
    db.session.add(newFaculty)
    db.session.commit()
    return newFaculty

def get_faculty(name):
    faculty = Faculty.query.filter_by(name=name).first()
    if not faculty:
        return False
    return faculty