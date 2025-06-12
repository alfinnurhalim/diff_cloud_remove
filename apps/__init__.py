from flask import Flask
from .routes.main import main_blueprint

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(main_blueprint)
    return app
