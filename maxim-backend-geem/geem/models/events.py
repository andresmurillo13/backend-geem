from tortoise import Model, fields


class ModelEvents(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200, null=False)
    reporter = fields.CharField(max_length=150, null=False)
    effectiv = fields.CharField(max_length=500, null=True)
    status = fields.IntField(null=False)
    property_damage = fields.BooleanField(default=False)
    cost = fields.IntField(null=False)
    created = fields.DatetimeField(auto_now=True, null=False)
    updated = fields.DatetimeField(null=True)
    closed = fields.DatetimeField(null=True)
    date = fields.DateField(null=False)
    date_close = fields.DateField(null=True)
    user = fields.ForeignKeyField('models.ModelUser', related_name="user_resp_event")
    eventtype = fields.ForeignKeyField('models.ModelEventtype', related_name="event_type")

    class Meta:
        table = 'events'