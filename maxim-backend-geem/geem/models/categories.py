from tortoise import Model, fields


class ModelCategories(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    available = fields.BooleanField(default=True)
    user = fields.ForeignKeyField("models.ModelUser")

    class Meta:
        table = 'categories'