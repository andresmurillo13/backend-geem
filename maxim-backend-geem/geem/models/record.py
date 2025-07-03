from tortoise import Model, fields


class ModelRecord(Model):
    id = fields.IntField(pk=True)
    activity = fields.CharField(max_length=100, null=True)
    date_done = fields.DateField()
    fluid_temperature = fields.CharField(max_length=20)
    drumm = fields.CharField(max_length=50, null=True)
    numbers_runs_current = fields.IntField(null=True)
    number_runs = fields.IntField()
    total_runs = fields.IntField()
    length_current = fields.IntField(null=True)
    length_cut = fields.IntField()
    length_final = fields.IntField()
    cause_cut = fields.CharField(max_length=200, null=True)
    depth_max = fields.IntField(null=True)
    strain_max = fields.IntField(null=True)
    swibelt_join = fields.CharField(max_length=100, null=True)
    length = fields.IntField(null=True)
    test_result = fields.CharField(max_length=150, null=True)
    obs = fields.CharField(max_length=250, null=True)
    types = fields.ForeignKeyField('models.ModelTypes')
    locations = fields.ForeignKeyField('models.ModelLocations')
    lineservices = fields.ForeignKeyField('models.ModelLineservices')
    user = fields.ForeignKeyField('models.ModelUser', related_name='operador')
    user_created = fields.ForeignKeyField('models.ModelUser', related_name='crea_record')
    tools = fields.ForeignKeyField('models.ModelTools', related_name='herramienta_record')
    tools_unit = fields.ForeignKeyField('models.ModelTools', related_name='unidad')

    class Meta:
        table = 'record'