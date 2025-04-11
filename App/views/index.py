from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import create_user, initialize, create_building
from App.models import db, Marker, Building, Faculty
from werkzeug.utils import secure_filename
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
        
        
@index_views.route('/', methods=['GET'])
def index_page():
    markers = Marker.query.all()
    markerCoords = []
    for marker in markers:
        #This code is pure heresy.
        markerCoords.append([marker.x, marker.y, marker.id, marker.name, marker.floor, marker.description, marker.building.name, marker.image])

    buildings = Building.query.all()
    faculties = Faculty.query.all()
    buildingData = []
    for building in buildings:
        buildingData.append([building.name, building.drawingCoords])
    return render_template('index.html', markers=markers, buildings=buildings, faculties=faculties)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/addMarker', methods=['POST'])
def add_marker():
    data = request.form
    imageFile = request.files['imageUpload']
        
    building = Building.query.get(data['buildingChoice'])
    if building:
        marker = building.addMarker(x=data['x'], y=data['y'], name=data['markerName'], floor=int(data['floorNum']), description=data['description'])
        if marker:
            if imageFile:
                secureFilename = upload_file(imageFile)
                marker.addImage("static/images/" + secureFilename)
            print("Successfully added marker to building")
        else:
            print("Could not add marker to building")
    else:
        print("Building does not exist")
    return redirect(request.referrer)

@index_views.route('/editMarker/<id>', methods=['POST'])
def edit_marker(id):
    marker = Marker.query.get(id)
    imageFile = request.files['imageUpload']
    
    if not marker:
        print("could not find marker")
        return redirect(request.referrer)
    data = request.form
    #This could probably be moved to a model function
    marker.name = data['markerName']
    marker.floor = data['floorNum']
    marker.description = data['description']
    marker.x = data['x']
    marker.y = data['y']
    secureFilename = upload_file(imageFile)
    marker.image = ("static/images/" + secureFilename)
    
    db.session.add(marker)
    db.session.commit()
    return redirect(request.referrer)
    
@index_views.route('/deleteMarker/<id>')
def delete_marker(id):
    #This could also probably be moved to a model function
    marker = Marker.query.get(id)
    if not marker:
        print("could not find marker")
        return redirect(request.referrer)
    db.session.delete(marker)
    db.session.commit()
    return redirect(request.referrer)

@index_views.route('/addBuilding', methods=['POST'])
def addBuilding():
    data = request.form
    print(data['buildingName'])
    print(data['facultyChoice'])
    print(json.dumps(data['geoJSON']))
    building = create_building(data['buildingName'], data['facultyChoice'], data['geoJSON'])
    if not building:
        print("Could not create building")
        return redirect(request.referrer)
    print("Successfully added building")
    return redirect(request.referrer)

@index_views.route('/addDrawing', methods=['POST'])
def addDrawing():
    data = request.form
    print(data['building'])
    building = Building.query.filter_by(name=data['building']).first()
    stringData = json.dumps(data['data'])
    building.addDrawing(stringData)
    return redirect(request.referrer)

