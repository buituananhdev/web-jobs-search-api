from marshmallow import Schema, fields

class ApplicantSchema(Schema):
    applicant_id = fields.Integer(dump_only=True)
    candidate_id = fields.Integer(required=True)
    job_id = fields.Integer(required=True)
