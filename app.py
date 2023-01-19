from flask import Flask
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pages.routes import pages as PagesBlueprint

load_dotenv()


def create_app():
    app = Flask('__name__')
    app.secret_key = os.environ.get('SECRET_KEY')
    client = MongoClient(os.environ.get('MONGO_DB'))
    app.db = client.get_default_database()

    app.register_blueprint(PagesBlueprint)
    return app


my_app = create_app()
