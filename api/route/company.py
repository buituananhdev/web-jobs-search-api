from flask import Blueprint, request, jsonify
from http import HTTPStatus
from api.models.database import db
from api.models.company import Company
from api.schemas.company_schema import CompanySchema

company_api = Blueprint('company_api', __name__)

@company_api.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = Company.query.all()
        company_schema = CompanySchema(many=True)
        company_list = company_schema.dump(companies)
        return jsonify({'companies': company_list})

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@company_api.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    try:
        company = Company.query.get(company_id)
        if company:
            company_schema = CompanySchema()
            return jsonify(company_schema.dump(company))
        else:
            return {'message': 'Company not found'}, HTTPStatus.NOT_FOUND

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@company_api.route('/companies', methods=['POST'])
def create_company():
    try:
        data = request.json

        # Validate input data using Marshmallow schema
        company_schema = CompanySchema()
        errors = company_schema.validate(data)

        if errors:
            return {'message': 'Validation error', 'errors': errors}, HTTPStatus.BAD_REQUEST

        new_company = Company(
            name=data['name'],
            description=data.get('description'),
            location=data.get('location'),
            account_id=int(data['account_id'])
        )

        db.session.add(new_company)
        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = company_schema.dump(new_company)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@company_api.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    try:
        company = Company.query.get(company_id)
        if not company:
            return {'message': 'Company not found'}, HTTPStatus.NOT_FOUND

        data = request.json  # Use request.json for JSON data

        # Validate input data using Marshmallow schema
        company_schema = CompanySchema()
        errors = company_schema.validate(data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        company.name = data.get('name', company.name)
        company.description = data.get('description', company.description)
        company.location = data.get('location', company.location)
        company.account_id = int(data.get('account_id', company.account_id))

        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = company_schema.dump(company)
        return jsonify(result)

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@company_api.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    try:
        company = Company.query.get(company_id)
        if not company:
            return {'message': 'Company not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(company)
        db.session.commit()

        return {'message': 'Company deleted successfully'}

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR
