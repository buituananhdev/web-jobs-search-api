from http import HTTPStatus
from flask import Blueprint, request, jsonify
from api.models.database import db
from api.models.account import Account
from api.models.company import Company
from api.models.candidate import Candidate
from api.schemas.account_schema import AccountSchema

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

account_api = Blueprint('account_api', __name__)

@account_api.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        # Validate input data using Marshmallow schema
        account_schema = AccountSchema()

        email = data['email']
        password = data['password']
        role = data['role']

        # Check if email is already registered
        if Account.query.filter_by(email=email).first():
            return {'message': 'Email is already registered'}, HTTPStatus.CONFLICT

        # Create a new account
        new_account = Account(email=email, password=password, role=role)
        db.session.add(new_account)
        db.session.commit()

        # Depending on the role, create a company or candidate
        if role == 'company':
            new_company = Company(
                name=data.get('name'),
                description=data.get('description'),
                location=data.get('location'),
                account_id=new_account.account_id
            )
            db.session.add(new_company)
            db.session.commit()

        elif role == 'candidate':
            new_candidate = Candidate(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                account_id=new_account.account_id
            )
            db.session.add(new_candidate)
            db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = account_schema.dump(new_account)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@account_api.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        email = data.get('email')
        password = data.get('password')

        # Kiểm tra xem email và mật khẩu có được cung cấp hay không
        if not email or not password:
            return {'message': 'Email and password are required'}, HTTPStatus.BAD_REQUEST

        # Kiểm tra xem tài khoản có tồn tại không và mật khẩu có đúng không
        account = Account.query.filter_by(email=email).first()
        if account and account.check_password(password):
            access_token = create_access_token(identity=account.email)
            return jsonify({'access_token': access_token}), HTTPStatus.OK
        else:
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED

    except Exception as e:
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@account_api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), HTTPStatus.OK

    except Exception as e:
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR
