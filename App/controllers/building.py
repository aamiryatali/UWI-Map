from App.models import Building
from App.database import db
from .marker import upload_file, get_clean_path_from_url, SUPABASE_BUCKET, supabase
from sqlalchemy.exc import IntegrityError
from flask import jsonify, current_app

def create_building(name, facultyID, drawingCoords, description):
    newBuilding = Building(name=name, facultyID=facultyID, drawingCoords=drawingCoords, description=description)
    try:
        db.session.add(newBuilding)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(e)
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
    building = create_building(data['buildingName'], data['facultyChoice'], data['geoJSON'], data['description'])
    if not building:
        return jsonify({'error': 'Could not create building'}), 400
    else:
        if imageFile:
            secureFilename = upload_file(imageFile)
            if secureFilename:
                building.addImage(secureFilename)
    return jsonify({'success': 'Building successfully added'}), 200

def edit_building(id, data, imageFile):
    building = Building.query.get(id)
    if not building:
        return jsonify({'error' : 'Building not found'}), 400
    
    building.name = data['buildingName']
    building.facultyID = data['facultyChoice']
    building.description  = data['description']
    if data['newDrawingCoords'] != "":
        building.drawingCoords = data['newDrawingCoords']
        
    if imageFile:
        if building.image != '':
            filename = building.image
            path = get_clean_path_from_url(filename)
            result = supabase.storage.from_(SUPABASE_BUCKET).remove([path])
            if not result:
                db.session.rollback()
                return jsonify({'error': "Could not delete image associated"}), 400
        secureFilename = upload_file(imageFile)
        building.addImage(secureFilename)
        
    try:
        db.session.add(building)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error' : 'Building already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : 'Could not edit building'}), 400
    return jsonify({'success' : 'Building information updated'}), 200

def delete_building(id):
    building = Building.query.get(id)
    default = Building.query.get(1)
    if not building:
        return jsonify({'error' : 'Building does not exist'}), 400

    if building.image != '':
        filename = building.image
        path = get_clean_path_from_url(filename)
        result = supabase.storage.from_(SUPABASE_BUCKET).remove([path])
        if not result:
            db.session.rollback()
            return jsonify({'error': "Could not delete image associated"}), 400
        
    for marker in building.markers:
        marker.buildingID = 1
        default.addMarker(marker.x, marker.y, marker.name, marker.floor, marker.description)
        db.session.add(marker)
        print(f'{marker.name} - {marker.buildingID}')
        
    db.session.delete(building)
    db.session.commit()
    return jsonify({'success': 'Building successfully deleted'}), 200