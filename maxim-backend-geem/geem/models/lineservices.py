from tortoise import Model, fields


class ModelLineservices(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    initial = fields.CharField(max_length=10, unique=True)
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'lineservices'