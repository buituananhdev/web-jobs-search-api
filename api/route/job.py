from flask import Blueprint, request, jsonify
from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from api.models.database import db
from api.models.job import Job
from api.models.candidate import Candidate
from api.models.applicant import Applicant
from api.schemas.job_schema import JobSchema
from api.schemas.candidate_schema import CandidateSchema

job_api = Blueprint('job_api', __name__)

@job_api.route('/jobs', methods=['GET'])
def get_filtered_jobs():
    try:
        company_id = int(request.args.get('companyId', 0))
        keyword = request.args.get('keyword', '').strip()
        location = request.args.get('location', 'all' if request.args.get('location') is None else '').strip()
        salary = request.args.get('salary', '0').strip()

        filtered_query = Job.query

        if keyword or location != 'all' or salary != '0' or company_id > 0:
            filtered_query = filtered_query.filter(
                or_(Job.title.ilike(f"%{keyword}%") if keyword else "",
                    Job.location == location if location != 'all' else "",
                    Job.company_id == company_id if company_id > 0 else "",
                    and_(Job.salary >= 10000000, Job.salary <= 25000000) if salary else ""
                )
            )

        jobs = filtered_query.all()

        job_schema = JobSchema(many=True)
        filtered_job_list = job_schema.dump(jobs)

        return jsonify({'jobs': filtered_job_list})

    except Exception as e:
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@job_api.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        job_schema = JobSchema()
        return jsonify(job_schema.dump(job))
    else:
        return {'message': 'Job not found'}, HTTPStatus.NOT_FOUND

@job_api.route('/jobs', methods=['POST'])
def create_job():
    try:
        data = request.json

        # Validate input data using Marshmallow schema
        job_schema = JobSchema()
        errors = job_schema.validate(data)
        
        if errors:
            return {'message': 'Validation error', 'errors': errors}, HTTPStatus.BAD_REQUEST

        # Handle salary conversion more gracefully
        try:
            salary = float(data.get('salary', 0))
        except ValueError:
            return {'message': 'Invalid salary format'}, HTTPStatus.BAD_REQUEST

        new_job = Job(
            title=data['title'],
            description=data['description'],
            requirements=data.get('requirements'),
            salary=salary,
            location=data.get('location'),
            company_id=int(data['company_id'])
        )

        db.session.add(new_job)
        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = job_schema.dump(new_job)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return {'message': f'Internal Server Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@job_api.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {'message': 'Job not found'}, HTTPStatus.NOT_FOUND

    try:
        data = request.json

        # Validate input data using Marshmallow schema
        job_schema = JobSchema()
        errors = job_schema.validate(data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        job.title = data.get('title', job.title)
        job.description = data.get('description', job.description)
        job.requirements = data.get('requirements', job.requirements)
        job.salary = float(data.get('salary', job.salary))
        job.location = data.get('location', job.location)
        job.company_id = int(data.get('company_id', job.company_id))

        db.session.commit()

        # Serialize the response using the Marshmallow schema
        result = job_schema.dump(job)
        return jsonify(result)

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@job_api.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {'message': 'Job not found'}, HTTPStatus.NOT_FOUND

    db.session.delete(job)
    db.session.commit()

    return {'message': 'Job deleted successfully'}

@job_api.route('/jobs/company/<int:company_id>', methods=['GET'])
def get_jobs_by_company(company_id):
    jobs = Job.query.filter_by(company_id=company_id).all()

    if not jobs:
        return {'message': 'No jobs found for the given company_id'}, HTTPStatus.NOT_FOUND

    job_schema = JobSchema(many=True)
    job_list = job_schema.dump(jobs)
    return jsonify({'jobs': job_list})


@job_api.route('/jobs/<int:job_id>/candidates', methods=['GET'])
def get_candidates_for_job(job_id):
    try:
        job = Job.query.get(job_id)

        if not job:
            return {'message': 'Job not found'}, HTTPStatus.NOT_FOUND

        # Retrieve candidates associated with the given job_id
        candidates = (
            Candidate.query
            .join(Applicant, Candidate.candidate_id == Applicant.candidate_id)
            .filter(Applicant.job_id == job_id)
            .options(joinedload(Candidate.account))  # Assuming you want to load associated Account as well
            .all()
        )

        # Serialize the response using the CandidateSchema
        candidate_schema = CandidateSchema(many=True)
        candidate_list = candidate_schema.dump(candidates)

        return jsonify({'candidates': candidate_list})

    except Exception as e:
        return {'message': f'Error: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR
