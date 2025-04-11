from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import create_user, initialize
from App.models import db, Marker, Building
from werkzeug.utils import secure_filename
import os
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')
           
#This function just checks that the file extension is in the list of allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
           
@index_views.route('/', methods=['GET'])
def index_page():
    markers = Marker.query.all()
    markerCoords = []
    for marker in markers:
        #This code is pure heresy.
        markerCoords.append([marker.x, marker.y, marker.id, marker.name, marker.floor, marker.description, marker.building.name, marker.image])

    buildings = Building.query.all()
    buildingData = []
    for building in buildings:
        buildingData.append([building.name, building.drawingCoords])
    return render_template('index.html', markers=markerCoords, buildings=buildingData, buildingObjects=buildings)

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
            #If file is valid
            if imageFile.filename != '' and imageFile and allowed_file(imageFile.filename):
                #Clean the filename
                filename = secure_filename(imageFile.filename)
                #Save the file to App/static/images
                imageFile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                #Add the path to the marker itself
                marker.addImage("static/images/" + filename)
            print("Successfully added marker to building")
        else:
            print("Could not add marker to building")
    else:
        print("Building does not exist")
    return redirect(request.referrer)

@index_views.route('/editMarker/<id>', methods=['POST'])
def edit_marker(id):
    marker = Marker.query.get(id)
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

@index_views.route('/addDrawing', methods=['POST'])
def addDrawing():
    data = request.json
    print(data['building'])
    building = Building.query.filter_by(name=data['building']).first()
    stringData = json.dumps(data['data'])
    building.addDrawing(stringData)
    return redirect(request.referrer)

