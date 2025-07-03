from tortoise import Model, fields


class ModelMaintenances(Model):
    id = fields.IntField(pk=True)
    closed = fields.DatetimeField(null=True)
    created = fields.DatetimeField(null=True)
    user_created = fields.ForeignKeyField('models.ModelUser', null=True, related_name='crea_maintenance')
    user_closed = fields.ForeignKeyField('models.ModelUser', null=True, related_name='cierra_maintenance')
    obs = fields.CharField(max_length=300)
    status = fields.BooleanField(default=True)
    status_end = fields.IntField()
    user = fields.ForeignKeyField('models.ModelUser', null=True, related_name='responsable_maintenance')
    request = fields.ForeignKeyField('models.ModelRequest')
    tools = fields.ForeignKeyField('models.ModelTools')
    cost = fields.IntField(default=0)
    days_bad = fields.IntField(default=0)
    compliance = fields.IntField(default=0)
    type_maintenance = fields.IntField(default=0)
    consecutive = fields.IntField(default=0)
    date_alert = fields.DateField(null=True)
    date_done = fields.DateField(null=True)

    class Meta:
        table = 'maintenances'