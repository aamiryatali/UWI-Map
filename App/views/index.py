from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import create_user, initialize
from App.models import db, Marker, Building
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    markers = Marker.query.all()
    markerCoords = []
    for marker in markers:
        markerCoords.append([marker.x, marker.y])

    buildings = Building.query.all()
    buildingData = []
    for building in buildings:
        buildingData.append([building.name, building.drawingCoords])
    return render_template('index.html', markers=markerCoords, buildings=buildingData)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/addMarker', methods=['POST'])
def add_marker():
    print("hi")
    data = request.json
    print(data['x'])
    marker = Marker(x=data['x'], y=data['y'], name="test", floor=1)
    if marker:
        db.session.add(marker)
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

