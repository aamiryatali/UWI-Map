import urllib.request
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app, flash, url_for
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, current_user as jwt_current_user
from App.controllers import (
    create_user, initialize, get_faculties,
    get_building, add_building, edit_building, delete_building, get_buildings,
    get_marker, add_marker, edit_marker, delete_marker, get_markers)
from werkzeug.exceptions import HTTPException
import os

index_views = Blueprint('index_views', __name__, template_folder='../templates')
        
@index_views.errorhandler(Exception)
def page_not_found(error):
    if isinstance(error, HTTPException):
        return jsonify({'error': f'{error}'}), 500
    return jsonify({'error': f'{error}'}), 500

@index_views.route('/', methods=['GET'])
def index_page():
    markers = get_markers()
    buildings = get_buildings()
    faculties = get_faculties()
    return render_template('guestIndex.html', markers=markers, buildings=buildings, faculties=faculties)

@index_views.route('/get-data', methods=['GET'])
def get_data():
    markers = get_markers()
    buildings = get_buildings()
    faculties = get_faculties()
    data = {
        'markers' : [marker.to_dict() for marker in markers],
        'buildings' : [building.to_dict() for building in buildings],
        'faculties' : [faculty.to_dict() for faculty in faculties]
    }
    return jsonify(data), 200

    
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
@jwt_required()
def addMarker():
    data = request.form
    #Get the image file
    imageFile = request.files['imageUpload']
    result = add_marker(data, imageFile)
    return result
    
@index_views.route('/editMarker/<id>', methods=['POST'])
@jwt_required()
def editMarker(id):
    imageFile = request.files['imageUpload']
    data = request.form
    result = edit_marker(id, data, imageFile)
    return result
    
@index_views.route('/deleteMarker/<id>')
@jwt_required()
def deleteMarker(id):
    result = delete_marker(id)
    return result

@index_views.route('/addBuilding', methods=['POST'])
@jwt_required()
def addBuilding():
    data = request.form
    #Get the image file
    imageFile = request.files['imageUpload']
    result = add_building(data, imageFile)
    return result

@index_views.route('/editBuilding/<id>', methods=['POST'])
@jwt_required()
def editBuilding(id):
    data = request.form
    imageFile = request.files['imageUpload']
    result = edit_building(id, data, imageFile)
    return result
    
@index_views.route('/deleteBuilding/<id>')
@jwt_required()
def deleteBuilding(id):
    result = delete_building(id)
    return result



