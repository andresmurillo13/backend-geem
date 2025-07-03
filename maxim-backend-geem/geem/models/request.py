from tortoise import Model, fields


class ModelRequest(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    alert_days = fields.IntField(default=0)
    date_alert = fields.DateField()
    is_prevent = fields.BooleanField(default=False)
    obs = fields.CharField(max_length=300, null=True)
    status = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser', related_name='responsable')
    tools = fields.ForeignKeyField('models.ModelTools')
    locations = fields.ForeignKeyField('models.ModelLocations')
    categories = fields.ForeignKeyField('models.ModelCategories')
    created = fields.DatetimeField(null=True)
    closed = fields.DatetimeField(null=True)
    user_created = fields.ForeignKeyField('models.ModelUser', related_name='crea', null=True)
    user_closed = fields.ForeignKeyField('models.ModelUser', related_name='cierra', null=True)
    date_done = fields.DateField(null=True)
    simaf = fields.ForeignKeyField('models.ModelAplication', null=True)

    class Meta:
        table = 'request'