from flask import Blueprint, request, jsonify
from http import HTTPStatus
from api.models.database import db
from api.models.applicant import Applicant

applicant_api = Blueprint('applicant_api', __name__)

@applicant_api.route('/applicants', methods=['GET'])
def get_applicants():
    applicants = Applicant.query.all()
    applicant_list = [{'applicant_id': applicant.applicant_id, 'candidate_id': applicant.candidate_id, 'job_id': applicant.job_id} for applicant in applicants]
    return jsonify({'applicants': applicant_list})

@applicant_api.route('/applicants/<int:applicant_id>', methods=['GET'])
def get_applicant(applicant_id):
    applicant = Applicant.query.get(applicant_id)
    if applicant:
        return jsonify(applicant.serialize())
    else:
        return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

@applicant_api.route('/applicants', methods=['POST'])
def create_applicant():
    data = request.form

    # Kiểm tra xem có đủ dữ liệu từ client không
    required_fields = ['candidate_id', 'job_id']
    if not all(field in data for field in required_fields):
        return {'message': 'Missing required fields'}, HTTPStatus.BAD_REQUEST

    new_applicant = Applicant(
        candidate_id=int(data['candidate_id']),
        job_id=int(data['job_id'])
    )

    db.session.add(new_applicant)
    db.session.commit()

    return jsonify(new_applicant.serialize()), HTTPStatus.CREATED

@applicant_api.route('/applicants/<int:applicant_id>', methods=['PUT'])
def update_applicant(applicant_id):
    applicant = Applicant.query.get(applicant_id)
    if not applicant:
        return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

    data = request.form
    applicant.candidate_id = int(data.get('candidate_id', applicant.candidate_id))
    applicant.job_id = int(data.get('job_id', applicant.job_id))

    db.session.commit()

    return jsonify(applicant.serialize())

@applicant_api.route('/applicants/<int:applicant_id>', methods=['DELETE'])
def delete_applicant(applicant_id):
    applicant = Applicant.query.get(applicant_id)
    if not applicant:
        return {'message': 'Applicant not found'}, HTTPStatus.NOT_FOUND

    db.session.delete(applicant)
    db.session.commit()

    return {'message': 'Applicant deleted successfully'}

@applicant_api.route('/applicants/candidate/<int:candidate_id>', methods=['GET'])
def get_applicants_by_candidate(candidate_id):
    applicants = Applicant.query.filter_by(candidate_id=candidate_id).all()

    if not applicants:
        return {'message': 'No applicants found for the given candidate_id'}, HTTPStatus.NOT_FOUND

    applicant_list = [{'applicant_id': applicant.applicant_id, 'candidate_id': applicant.candidate_id, 'job_id': applicant.job_id} for applicant in applicants]
    return jsonify({'applicants': applicant_list})

