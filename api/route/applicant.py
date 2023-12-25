from flask import Blueprint, request, jsonify
from http import HTTPStatus
from api.models.database import db
from api.models.applicant import Applicant
from api.schemas.applicant_schema import ApplicantSchema

applicant_api = Blueprint('applicant_api', __name__)

@applicant_api.route('/applicants', methods=['GET'])
def get_applicants():
    try:
        applicants = Applicant.query.all()
        applicant_schema = ApplicantSchema(many=True)
        applicant_list = applicant_schema.dump(applicants)
        return jsonify({'applicants': applicant_list})

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants/<int:applicant_id>', methods=['GET'])
def get_applicant(applicant_id):
    try:
        applicant = Applicant.query.get(applicant_id)
        if applicant:
            applicant_schema = ApplicantSchema()
            return jsonify(applicant_schema.dump(applicant))
        else:
            return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants', methods=['POST'])
def create_applicant():
    try:
        data = request.json  # Use request.json for JSON data

        # Validate input data using Marshmallow schema
        applicant_schema = ApplicantSchema()
        errors = applicant_schema.validate(data)

        if errors:
            return {'message': 'Validation error', 'errors': errors}, HTTPStatus.BAD_REQUEST

        new_applicant = Applicant(
            candidate_id=int(data['candidate_id']),
            job_id=int(data['job_id'])
        )

        db.session.add(new_applicant)
        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = applicant_schema.dump(new_applicant)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants/<int:applicant_id>', methods=['PUT'])
def update_applicant(applicant_id):
    try:
        applicant = Applicant.query.get(applicant_id)
        if not applicant:
            return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

        data = request.json  # Use request.json for JSON data

        # Validate input data using Marshmallow schema
        applicant_schema = ApplicantSchema()
        errors = applicant_schema.validate(data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        applicant.candidate_id = int(data.get('candidate_id', applicant.candidate_id))
        applicant.job_id = int(data.get('job_id', applicant.job_id))

        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = applicant_schema.dump(applicant)
        return jsonify(result)

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants/<int:applicant_id>', methods=['DELETE'])
def delete_applicant(applicant_id):
    try:
        applicant = Applicant.query.get(applicant_id)
        if not applicant:
            return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(applicant)
        db.session.commit()

        return {'message': 'Applicant deleted successfully'}

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants/candidate/<int:candidate_id>', methods=['GET'])
def get_applicants_by_candidate(candidate_id):
    try:
        applicants = Applicant.query.filter_by(candidate_id=candidate_id).all()

        if not applicants:
            return {'message': 'No applicants found for the given candidate_id'}, HTTPStatus.NOT_FOUND

        applicant_schema = ApplicantSchema(many=True)
        applicant_list = applicant_schema.dump(applicants)
        return jsonify({'applicants': applicant_list})

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@applicant_api.route('/applicants/job/<int:job_id>', methods=['GET'])
def get_applicants_by_job(job_id):
    try:
        applicants = Applicant.query.filter_by(job_id=job_id).all()

        if not applicants:
            return {'message': 'No applicants found for the given job_id'}, HTTPStatus.NOT_FOUND

        applicant_schema = ApplicantSchema(many=True)
        applicant_list = applicant_schema.dump(applicants)
        return jsonify({'applicants': applicant_list})

    except Exception as e:
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR
