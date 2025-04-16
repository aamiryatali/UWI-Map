import os

UPLOAD_FOLDER = 'App/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
        delta = 7
        if config['ENV'] == "PRODUCTION":
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
            app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')
        else:
            app.config.from_object('App.default_config')
            
    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
    app.config['UPLOADED_FILES_DEST'] = UPLOAD_FOLDER
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    for key in overrides:
        app.config[key] = overrides[key]