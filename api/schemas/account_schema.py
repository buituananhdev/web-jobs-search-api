from marshmallow import Schema, fields

class AccountSchema(Schema):
    account_id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)
