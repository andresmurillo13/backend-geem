from tortoise import Model, fields


class ModelFixedlineitems(Model):
    position = fields.IntField()
    optional = fields.BooleanField(default=True)
    fixedline = fields.ForeignKeyField('models.ModelFixedline')
    docversion = fields.ForeignKeyField('models.ModelDocversion')

    class Meta:
        table = 'fixedlineitems'