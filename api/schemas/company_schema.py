from marshmallow import Schema, fields, validate

class CompanySchema(Schema):
    company_id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    location = fields.String()
    account_id = fields.Integer(required=True)