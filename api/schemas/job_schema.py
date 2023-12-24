from marshmallow import Schema, fields

class JobSchema(Schema):
    job_id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    requirements = fields.String()
    salary = fields.Decimal(places=2)
    location = fields.String()
    company_id = fields.Integer(required=True)
