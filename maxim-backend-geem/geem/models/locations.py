from tortoise import Model, fields


class ModelLocations(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    description = fields.CharField(max_length=100)
    status = fields.BooleanField(default=True)
    typewells = fields.ForeignKeyField('models.ModelTypewells')
    fields = fields.ForeignKeyField('models.ModelFields')

    class Meta:
        table = 'locations'