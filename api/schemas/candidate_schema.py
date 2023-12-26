from marshmallow import Schema, fields, validate

class CandidateSchema(Schema):
    candidate_id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    name = fields.String(required=True)
    phone = fields.String(required=True)
    account_id = fields.Integer(required=True)