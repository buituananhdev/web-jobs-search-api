from datetime import timedelta
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager
from flask import Flask
from api.route.account import account_api
from api.route.job import job_api
from api.route.company import company_api

from api.models.database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    CORS(app)
    db.init_app(app)  # Use the existing db instance created in models/account.py
    with app.app_context():
        db.create_all()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    # Initialize Config
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY") # Thay thế bằng một khóa bí mật thực tế

    jwt = JWTManager(app)
    app.config.from_pyfile('config.py')
    
    # Register Blueprints
    app.register_blueprint(account_api, url_prefix='/api')
    app.register_blueprint(job_api, url_prefix='/api')
    app.register_blueprint(company_api, url_prefix='/api')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3014, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
