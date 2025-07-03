from tortoise import Model, fields


class ModelTypewells(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'typewells'