from tortoise import Model, fields


class Modelpqrstype(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'pqrstype'