from tortoise import Model, fields


class ModelTypes(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    type = fields.IntField()
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'types'