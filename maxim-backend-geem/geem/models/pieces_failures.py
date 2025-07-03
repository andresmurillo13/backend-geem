from tortoise import Model, fields


class ModelPiecesFailures(Model):
    id = fields.IntField(pk=True)
    status = fields.BooleanField(default=True)
    request = fields.ForeignKeyField('models.ModelRequest')
    pieces = fields.ForeignKeyField('models.ModelPieces')
    failures = fields.ForeignKeyField('models.ModelFailures')
    maintenances = fields.ForeignKeyField('models.ModelMaintenances', null=True)
    created = fields.DatetimeField(null=True)
    closed = fields.DatetimeField(null=True)

    class Meta:
        table = 'piecesfailures'