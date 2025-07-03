from tortoise import Model, fields


class ModelAplication(Model):
    id = fields.IntField(pk=True)
    started = fields.DatetimeField(null=True)
    ended = fields.DatetimeField(null=True)
    obs = fields.CharField(null=True, max_length=200)
    status = fields.BooleanField(default=True)
    workplan = fields.ForeignKeyField('models.ModelWorkplan')
    user = fields.ForeignKeyField('models.ModelUser')
    locations = fields.ForeignKeyField('models.ModelLocations')
    fields = fields.ForeignKeyField('models.ModelFields')

    class Meta:
        table = 'aplication'