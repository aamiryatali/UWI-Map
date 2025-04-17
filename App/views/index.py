import urllib.request
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app, flash, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from sqlalchemy.exc import IntegrityError
from App.controllers import create_user, initialize, create_building, get_marker, get_building
from App.models import db, Marker, Building, Faculty
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import os
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

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
        
@index_views.errorhandler(Exception)
def page_not_found(error):
    if isinstance(error, HTTPException):
        return jsonify({'error': f'{error}'}), 500
    return jsonify({'error': f'{error}'}), 500

@index_views.route('/', methods=['GET'])
def index_page():
    markers = Marker.query.all()
    buildings = Building.query.all()
    faculties = Faculty.query.all()
    return render_template('index.html', markers=markers, buildings=buildings, faculties=faculties)

@index_views.route('/get-data', methods=['GET'])
def get_data():
    markers = Marker.query.all()
    buildings = Building.query.all()
    faculties = Faculty.query.all()
    return jsonify({
        'markers' : [marker.to_dict() for marker in markers],
        'buildings' : [building.to_dict() for building in buildings],
        'faculties' : [faculty.to_dict() for faculty in faculties]
    })

    
@index_views.route('/init', methods=['GET'])
def init():
    if os.environ.get("ENV") == "PRODUCTION":
        flash('Server is currently running in production mode, initialize blocked')
        return redirect(url_for('index_views.index_page'))
    elif os.environ.get("ENV") == "DEVELOPMENT":
        initialize()
        return jsonify(message='db initialized!')
    elif os.environ.get("ENV") == "PRODUCTIONINIT":
        initialize()
        return jsonify(message='db initialized!')
    flash('Could not get deployment type(PRODUCTION/DEVELOPMENT)')
    return redirect(url_for('index_views.index_page'))

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/addMarker', methods=['POST'])
def add_marker():
    data = request.form
    if get_marker(data['markerName']):
        return jsonify({'error': "Marker name already exists!"}), 400
    
    #Get the image file
    imageFile = request.files['imageUpload']
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

@index_views.route('/editMarker/<id>', methods=['POST'])
def edit_marker(id):
    marker = Marker.query.get(id)
    if not marker:
        return jsonify({'error': "Could not find marker"}), 400
    
    imageFile = request.files['imageUpload']
    data = request.form
    #This could probably be moved to a model function
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
    
@index_views.route('/deleteMarker/<id>')
def delete_marker(id):
    #This could also probably be moved to a model function
    marker = Marker.query.get(id)
    if not marker:
        return jsonify({'error': "Marker does not exist"}), 400
    db.session.delete(marker)
    db.session.commit()
    return jsonify({'success' : "Marker information updated!"}), 200

@index_views.route('/addBuilding', methods=['POST'])
def addBuilding():
    data = request.form
    if get_building(data['buildingName']):
        return jsonify({'error': 'Building name already exists!'}), 400
    
    #Get the image file
    imageFile = request.files['imageUpload']
    
    print(data['buildingName'])
    print(data['facultyChoice'])
    print(json.dumps(data['geoJSON']))
    building = create_building(data['buildingName'], data['facultyChoice'], data['geoJSON'])
    if not building:
        return jsonify({'error': 'Could not create building'}), 400
    else:
        if imageFile:
            secureFilename = upload_file(imageFile)
            if secureFilename:
                building.addImage("static/images/" + secureFilename)
    return jsonify({'success': 'Building successfully added'}), 200

@index_views.route('/editBuilding/<id>', methods=['POST'])
def editBuilding(id):
    building = Building.query.get(id)
    if not building:
        return jsonify({'error' : 'Building not found'}), 400
    
    data = request.form
    imageFile = request.files['imageUpload']
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
    
@index_views.route('/deleteBuilding/<id>')
def deleteBuilding(id):
    #This could also probably be moved to a model function
    building = Building.query.get(id)
    default = Building.query.get(1)
    if not building:
        return jsonify({'error' : 'Building does not exist'}), 400
    for marker in building.markers:
        default.addMarker(marker.x, marker.y, marker.name, marker.floor, marker.description)
        print(f'${marker.name} + ${marker.buildingID}')
        marker.buildingID = 1
        print(f'${marker.name} + ${marker.buildingID}')
        db.session.add(marker)
    db.session.delete(building)
    db.session.commit()
    return jsonify({'success': 'Building successfully deleted'}), 200
    


