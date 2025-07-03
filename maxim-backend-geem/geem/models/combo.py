from tortoise import Model, fields


class ModelCombo(Model):
    id = fields.IntField(pk=True)
    locations = fields.ForeignKeyField('models.ModelLocations')
    tools_unit = fields.ForeignKeyField('models.ModelTools')
    combo_tools = fields.ManyToManyField('models.ModelTools', related_name='asignacion_combo')

    class Meta:
        table = 'combo'