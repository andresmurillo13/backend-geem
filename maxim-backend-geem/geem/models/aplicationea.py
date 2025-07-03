from tortoise import Model, fields


class ModelAplicationea(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True, null=False)
    changed = fields.DatetimeField(null=True)
    status = fields.BooleanField(default=True)
    block = fields.BooleanField(default=False)
    is_use = fields.BooleanField(default=False)
    aplication = fields.ForeignKeyField('models.ModelAplication')
    tools = fields.ForeignKeyField('models.ModelTools')

    class Meta:
        table = 'aplicationea'