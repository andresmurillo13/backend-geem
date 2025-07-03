from meliodas.model import Model


class Blacklist(Model):
    _model = 'blacklist'

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', None)
        self._ip = kwargs.get('ip', None)
        self._created = kwargs.get('created', None)
        self._reason = kwargs.get('reason', None)
        self._path = kwargs.get('path', None)
        self._updated = kwargs.get('updated', None)
        self._is_active = kwargs.get('is_active', None)

    @property
    def reason(self):
        return self._reason
