from tortoise import Model, fields


class ModelDocversion(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True, null=False)
    deleted = fields.DatetimeField(null=True)
    name = fields.CharField(max_length=100, null=False)
    description = fields.CharField(max_length=200, null=True)
    url = fields.CharField(max_length=200, null=True)
    doccode = fields.CharField(max_length=45, null=False)
    status = fields.IntField()
    version = fields.CharField(max_length=45, null=False)

    class Meta:
        table = 'docversion'