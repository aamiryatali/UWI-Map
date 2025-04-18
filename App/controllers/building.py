from App.models import Building
from App.database import db
from .marker import upload_file, allowed_file
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import jsonify, current_app
import os

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

def get_buildings():
    return Building.query.all()

def add_building(data, imageFile):
    if get_building(data['buildingName']):
        return jsonify({'error': 'Building name already exists!'}), 400
    building = create_building(data['buildingName'], data['facultyChoice'], data['geoJSON'])
    if not building:
        return jsonify({'error': 'Could not create building'}), 400
    else:
        if imageFile:
            secureFilename = upload_file(imageFile)
            if secureFilename:
                building.addImage("static/images/" + secureFilename)
    return jsonify({'success': 'Building successfully added'}), 200

def edit_building(id, data, imageFile):
    building = Building.query.get(id)
    if not building:
        return jsonify({'error' : 'Building not found'}), 400
    
    building.name = data['buildingName']
    building.facultyID = data['facultyChoice']
    if data['newDrawingCoords'] != "":
        building.drawingCoords = data['newDrawingCoords']
    if imageFile:
            secureFilename = upload_file(imageFile)
            building.addImage("static/images/" + secureFilename)
    try:
        db.session.add(building)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error' : 'Building name already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : 'Could not edit building'}), 400
    return jsonify({'success' : 'Building information updated'}), 200

def delete_building(id):
    building = Building.query.get(id)
    default = Building.query.get(1)
    if not building:
        return jsonify({'error' : 'Building does not exist'}), 400

    for marker in building.markers:
        marker.buildingID = 1
        default.addMarker(marker.x, marker.y, marker.name, marker.floor, marker.description)
        db.session.add(marker)
        print(f'{marker.name} - {marker.buildingID}')
        
    db.session.delete(building)
    db.session.commit()
    return jsonify({'success': 'Building successfully deleted'}), 200