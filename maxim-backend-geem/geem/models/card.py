from tortoise import Model, fields


class ModelCard(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField()
    created = fields.DatetimeField()
    closed = fields.DatetimeField(null=True)
    document = fields.CharField(max_length=20, null=True)
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=150, null=True)
    company = fields.CharField(max_length=100, null=True)
    position = fields.CharField(max_length=100, null=True)
    obs = fields.CharField(max_length=1000)
    action = fields.CharField(max_length=1000)
    close = fields.CharField(max_length=1000, null=True)
    site = fields.CharField(max_length=100)
    status = fields.IntField()
    zone = fields.IntField()
    areas = fields.ForeignKeyField('models.ModelAreas', null=True)
    user = fields.ForeignKeyField('models.ModelUser', related_name="user_created_card")
    user_obs = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_obs")
    user_resp = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_resp_card")
    user_boss = fields.ForeignKeyField('models.ModelUser', related_name="user_boss_card")
    companies = fields.ForeignKeyField('models.ModelCompanies', null=True)
    items = fields.ManyToManyField('models.ModelVersionitems', related_name='asignacion_versionitem')
    simaf = fields.ForeignKeyField('models.ModelAplication', null=True)
    locations = fields.ForeignKeyField('models.ModelLocations', null=True)

    class Meta:
        table = 'card'