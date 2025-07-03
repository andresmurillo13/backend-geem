from tortoise import Model, fields


class ModelEnlistmentslog(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True)
    status_new = fields.IntField()
    status_last = fields.IntField(null=True)
    obs = fields.CharField(null=True, max_length=200)
    user = fields.ForeignKeyField('models.ModelUser')
    enlistments = fields.ForeignKeyField('models.ModelEnlistments')
    enlistment_type = fields.IntField(default=1)
    date = fields.DateField(auto_now=True, null=True)

    class Meta:
        table = 'enlistmentslog'