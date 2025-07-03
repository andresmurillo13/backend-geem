from tortoise import Model, fields


class ModelNames(Model):
    id = fields.IntField(pk=True)
    initial = fields.CharField(max_length=10)
    cost_cert = fields.IntField(null=True)
    cost_mant = fields.IntField(null=True)
    cost_otm = fields.IntField(null=True)
    aspect = fields.TextField(null=True)
    recomendation = fields.TextField(null=True)
    reposition = fields.TextField(null=True)
    disposition = fields.TextField(null=True)
    critery = fields.TextField(null=True)
    live = fields.TextField(null=True)
    available = fields.BooleanField(default=True)
    descriptionnames = fields.ForeignKeyField('models.ModelDescriptionnames')
    types = fields.ForeignKeyField('models.ModelTypes')
    pieces = fields.ManyToManyField('models.ModelPieces')

    class Meta:
        table = 'names'