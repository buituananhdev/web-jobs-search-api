from datetime import timedelta
import os
from flask import Flask
from flasgger import Swagger
from api.route.account import account_api
from api.route.job import job_api
from api.models.database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    
    db.init_app(app)  # Use the existing db instance created in models/account.py
    with app.app_context():
        db.create_all()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    # Initialize Config
    app.config.from_pyfile('config.py')
    
    # Register Blueprints
    app.register_blueprint(account_api, url_prefix='/api')
    app.register_blueprint(job_api, url_prefix='/api')


    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
