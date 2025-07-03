from tortoise import Model, fields


class ModelFilesFindings(Model):
    id = fields.IntField(pk=True)
    path_complete = fields.CharField(max_length=500)
    name = fields.CharField(max_length=200)
    created = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser')
    chatevents = fields.ForeignKeyField('models.ModelChatevents', null=True)
    findings = fields.ForeignKeyField('models.ModelFindings', null=True)
    events = fields.ForeignKeyField('models.ModelEvents', null=True)
    task_events = fields.ForeignKeyField('models.ModelTaskevents', null=True)

    class Meta:
        table = 'filesfindings'
