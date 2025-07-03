from tortoise import Model, fields


class ModelJoblog(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True, null=False)
    ended = fields.DatetimeField(null=True)
    active = fields.BooleanField(default=True)
    timeline = fields.ForeignKeyField('models.ModelTimeline')
    joblogusers = fields.ManyToManyField('models.ModelUser', related_name='joblogusers')
    joblogequipments = fields.ManyToManyField('models.ModelTools', related_name='joblogequipments', through='joblog_equipments')
    joblogtools = fields.ManyToManyField('models.ModelTools', related_name='joblogtools', through='joblog_tools')

    class Meta:
        table = 'joblog'