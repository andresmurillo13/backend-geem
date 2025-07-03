from tortoise import Model, fields


class ModelFields(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    description = fields.CharField(max_length=150)
    status = fields.BooleanField(default=True)
    gerencies = fields.ForeignKeyField('models.ModelGerencies')

    class Meta:
        table = 'fields'