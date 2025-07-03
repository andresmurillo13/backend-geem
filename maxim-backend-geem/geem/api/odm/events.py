from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID

class CreateEventODM(Schema):

    description = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    reporter = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    effectiv = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    date = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    cost = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    event_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    property_damage = fields.Boolean(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class UpdateEventODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    description = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    reporter = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    effectiv = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    date = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    cost = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    event_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    status = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    property_damage = fields.Boolean(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    date_close = fields.Date(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )


class UseEventODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )


class GetEventUser(Schema):

    key = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    type = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    status = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    page = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class CloseEventODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    effectiv = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    date_close = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )




