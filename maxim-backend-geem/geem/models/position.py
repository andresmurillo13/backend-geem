from tortoise import Model, fields


class ModelPosition(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    status = fields.BooleanField(default=True)
    areas = fields.ManyToManyField('models.ModelAreas')

    class Meta:
        table = 'position'