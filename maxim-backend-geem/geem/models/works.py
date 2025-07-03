from tortoise import Model, fields


class ModelWorks(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    created = fields.DatetimeField(auto_now_add=True)
    obs = fields.CharField(max_length=300)
    user = fields.ForeignKeyField('models.ModelUser')
    tools = fields.ForeignKeyField('models.ModelTools', related_name='herramienta')
    tools_unit = fields.ForeignKeyField('models.ModelTools', related_name='herramienta_unidad')
    locations = fields.ForeignKeyField('models.ModelLocations')
    categories = fields.ForeignKeyField('models.ModelCategories', null=True)

    class Meta:
        table = 'works'