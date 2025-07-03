from tortoise import Model, fields


class ModelToolstring(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    hours_work = fields.IntField()
    max_tension = fields.IntField(null=True)
    max_deep = fields.IntField(null=True)
    types = fields.ForeignKeyField('models.ModelTypes')
    locations = fields.ForeignKeyField('models.ModelLocations')
    tools = fields.ForeignKeyField('models.ModelTools', related_name='herramienta_toolstring')
    tools_toolstring = fields.ManyToManyField('models.ModelTools', related_name='asignacion_toolstring')

    class Meta:
        table = 'toolstring'