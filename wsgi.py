import click, pytest, sys
from flask import Flask, jsonify
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Marker, Building, Faculty
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_building)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
# Commenting this out so someone doesn't accidently wipe the database
#@app.cli.command("init", help="Creates and initializes the database")
#def init():
#    initialize()
#    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 
debug_cli = AppGroup('debug', help='Show useful commands for debugging')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user(admin). This user can login to edit the map.")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli
app.cli.add_command(debug_cli)

@debug_cli.command("list-markers", help="Lists markers in the database")
def list_user_command():
    list = Marker.query.all()
    for m in list:
        print(f'{m.name} | {m.x} | {m.y} | {m.image} | {m.buildingID}')
        

app.cli.add_command(debug_cli) # add the group to the cli

@debug_cli.command('list-buildings', help="Lists the buildings in the database")
def list_buildings_command():
    buildings = Building.query.all()
    for building in buildings:
       print(f'{building.name} | {building.image} | {building.faculty.name}')

app.cli.add_command(debug_cli)

@debug_cli.command('list-building-markers', help="Lists all the markers that belong to a building")
@click.argument('building_name', default='N/A')
def list_building_markers_command(building_name):
    building = Building.query.filter_by(name=building_name).first()
    if not building:
        print("Building does not exist")
    else:
        for m in building.markers:
            print(f'{m.name} | {m.x} | {m.y} | {m.image}')
app.cli.add_command(debug_cli)

@debug_cli.command('get-data')
def get_cli_data():
    markers = Marker.query.all()
    buildings = Building.query.all()
    faculties = Faculty.query.all()
    data = {
        'markers' : [marker.to_dict() for marker in markers],
        'buildings' : [building.to_dict() for building in buildings],
        'faculties' : [faculty.to_dict() for faculty in faculties]
    }
    jsonData = jsonify(data)
    print(jsonData)


app.cli.add_command(debug_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)