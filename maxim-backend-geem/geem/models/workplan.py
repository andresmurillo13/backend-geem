from tortoise import Model, fields


class ModelWorkplan(Model):
    id = fields.IntField(pk=True)
    typeservice = fields.IntField()
    description = fields.CharField(max_length=200)
    created = fields.DatetimeField(auto_now=True)
    started = fields.DatetimeField(null=True)
    ended = fields.DatetimeField(null=True)
    planneddate = fields.DateField()
    enddate = fields.DateField()
    status = fields.IntField(defaul=1)
    obs = fields.CharField(null=True, max_length=200)
    servicerequest = fields.ForeignKeyField('models.ModelServicerequest')
    lineservices = fields.ForeignKeyField('models.ModelLineservices')
    user = fields.ForeignKeyField('models.ModelUser')
    userresp = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_resp_workplan")


    class Meta:
        table = 'workplan'