from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptEquityResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    transcript_id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    date = fields.DateTime(required=True)
    updated_at = fields.DateTime()
