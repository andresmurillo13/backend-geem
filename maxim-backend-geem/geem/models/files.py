from tortoise import Model, fields


class ModelFiles(Model):
    id = fields.IntField(pk=True)
    path_complete = fields.CharField(max_length=500)
    name = fields.CharField(max_length=200)
    created = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser')
    request = fields.ForeignKeyField('models.ModelRequest', null=True)
    tools = fields.ForeignKeyField('models.ModelTools', null=True)
    maintenances = fields.ForeignKeyField('models.ModelMaintenances', null=True)
    record = fields.ForeignKeyField('models.ModelRecord', null=True, related_name='file_record')
    toolstring = fields.ForeignKeyField('models.ModelToolstring', null=True)
    record_info = fields.ForeignKeyField('models.ModelTools', null=True, related_name='file_record_info')

    class Meta:
        table = 'files'
