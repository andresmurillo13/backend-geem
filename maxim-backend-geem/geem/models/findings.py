from tortoise import Model, fields


class ModelFindings(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=500, null=False)
    correction = fields.CharField(max_length=500, null=True)
    repeated = fields.BooleanField(null=False)
    status = fields.IntField(null=False)
    created = fields.DatetimeField(auto_now=True, null=False)
    updated = fields.DatetimeField(null=True)
    closed = fields.DatetimeField(null=True)
    effectiv = fields.CharField(max_length=500, null=True)
    user = fields.ForeignKeyField('models.ModelUser', related_name="user_resp_finding")
    actiontype = fields.ForeignKeyField('models.ModelActiontype', related_name="action_type")
    findingtype = fields.ForeignKeyField('models.ModelFindingtype', related_name="finding_type")
    location = fields.ForeignKeyField('models.ModelLocations', related_name="location")
    area = fields.ForeignKeyField('models.ModelAreas', related_name="area_findings")
    event = fields.ForeignKeyField('models.ModelEvents', related_name="event")


    class Meta:
        table = 'findings'