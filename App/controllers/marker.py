from App.models import Marker, Building
from App.database import db
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import jsonify, current_app
import os

#This function just checks that the file extension is in the list of allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
           
def upload_file(imageFile):
    if imageFile.filename != '' and imageFile and allowed_file(imageFile.filename):
        #Clean the filename
        filename = secure_filename(imageFile.filename)
        #Save the file to App/static/images(We may have to consider uploading pictures to a 3rd party host as 
        #OnRender doesn't provide us any persistent storage on the free tier)
        imageFile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
    
def get_marker(name):
    marker = Marker.query.filter_by(name=name).first()
    if marker:
        return marker
    return False

def get_markers():
    return Marker.query.all()

def add_marker(data, imageFile):
    if get_marker(data['markerName']):
        return jsonify({'error': "Marker name already exists!"}), 400
    building = Building.query.get(data['buildingChoice'])
    if building:
        marker = building.addMarker(x=data['x'], y=data['y'], name=data['markerName'], floor=int(data['floorNum']), description=data['description'])
        if marker:
            if imageFile:
                secureFilename = upload_file(imageFile)
                if secureFilename:
                    marker.addImage("static/images/" + secureFilename)
            return jsonify({'success': 'Marker successfully added!'}), 200
        else:
            return jsonify({'error': 'Could not add marker to building!'}), 400
    return jsonify({'error': 'Building does not exist!'}), 400

def edit_marker(id, data, imageFile):
    marker = Marker.query.get(id)
    if not marker:
        return jsonify({'error': "Could not find marker"}), 400

    marker.name = data['markerName']
    marker.floor = data['floorNum']
    marker.description = data['description']
    marker.buildingID = data['buildingChoice']
    marker.x = data['x']
    marker.y = data['y']
    if imageFile:
        secureFilename = upload_file(imageFile)
        marker.image = ("static/images/" + secureFilename)
    
    try:
        db.session.add(marker)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': "Marker name already exists!"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': "Unable to edit marker"}), 400
    return jsonify({'success' : "Marker information updated!"}), 200

def delete_marker(id):
    marker = Marker.query.get(id)
    if not marker:
        return jsonify({'error': "Marker does not exist"}), 400
    db.session.delete(marker)
    db.session.commit()
    return jsonify({'success' : "Marker successfully deleted!"}), 200