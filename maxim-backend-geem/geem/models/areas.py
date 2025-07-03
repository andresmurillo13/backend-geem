from tortoise import Model, fields


class ModelAreas(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)
    pqrs = fields.BooleanField(default=False)
    status = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser')

    class Meta:
        table = 'areas'