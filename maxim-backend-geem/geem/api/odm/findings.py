from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID

class CreateFindingODM(Schema):

    description = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    correction = fields.Str(
        required=False,
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

    repeated = fields.Boolean(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    action_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    finding_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    events = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    locations = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    areas = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class UpdateFindingODM(Schema):

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

    effectiv = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    correction = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    repeated = fields.Boolean(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    action_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    finding_type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    events = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    locations = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    areas = fields.Int(
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


class UseFindingODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )


class GetFindingUser(Schema):

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

    event = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class DeliverFindingODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    correction = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class CloseFindingODM(Schema):

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







