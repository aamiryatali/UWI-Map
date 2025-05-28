from App.models import Marker, Building
from App.database import db
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import jsonify, current_app, request
from supabase import create_client, Client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
 
#This function just checks that the file extension is in the list of allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
           
def upload_file(imageFile):
    if imageFile.filename != '' and imageFile and allowed_file(imageFile.filename):
        #Clean the filename
        filename = secure_filename(imageFile.filename)
        #Save the file to Supabase
        result = supabase.storage.from_(SUPABASE_BUCKET).upload(
            filename,
            imageFile.read(),
            {"content-type": imageFile.mimetype}
        )
        if not result:
            return None

        url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
        return url
    return None
    
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
                    marker.addImage(secureFilename)
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
        if marker.image != '':
            filename = marker.image
            path = get_clean_path_from_url(filename)
            result = supabase.storage.from_(SUPABASE_BUCKET).remove([path]) #Remove any old image
            if not result:
                db.session.rollback()
                return jsonify({'error': "Could not delete image associated"}), 400
        secureFilename = upload_file(imageFile) #Then add the new one
        marker.image = secureFilename
    
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

#The superbase URL to the file(which is what we store in the db) actually has a ? at the end. But we need the filename
#to delete the file. This function just removes the ? and grabs the filename by parsing the path format supabase uses for storage.
def get_clean_path_from_url(file_url):
    clean_url = file_url.split("?")[0]  
    return clean_url.split("/object/public/")[1].split("/", 1)[1]

def delete_marker(id):
    marker = Marker.query.get(id)
    if marker.image != '':
        filename = marker.image
        path = get_clean_path_from_url(filename)
        result = supabase.storage.from_(SUPABASE_BUCKET).remove([path])
        if not result:
            db.session.rollback()
            return jsonify({'error': "Could not delete image associated"}), 400
    if not marker:
        return jsonify({'error': "Marker does not exist"}), 400
    db.session.delete(marker)
    db.session.commit()
    return jsonify({'success' : "Marker successfully deleted!"}), 200