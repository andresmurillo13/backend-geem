import asyncio
from datetime import datetime, timedelta

from meliodas.model import Model

from security.models import Blacklist
from security.settings import MAX_COUNT
from security.utils import log_debug, send_message_alert


class BlacklistAlert(Model):
    _model = 'blacklist_alert'

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', None)
        self._ip = kwargs.get('ip', None)
        self._created = kwargs.get('created', None)
        self._count = kwargs.get('count', 1)
        self._path = kwargs.get('path', None)
        self._updated = kwargs.get('updated', None)

    @property
    def id(self):
        return self._id

    @property
    def count(self):
        return self._count

    @classmethod
    async def register_alert(cls, ip, reason, path):
        updated = datetime.today()
        last_minute = updated - timedelta(minutes=1)
        alert = await cls.get_or_none(ip=ip, created={'$gte': last_minute}, path=path)
        if alert:
            count = alert.count + 1
            await cls.update(_id=alert.id, count=count, updated=updated)
            if count >= int(MAX_COUNT):
                blacklist = await Blacklist.get_or_none(ip=ip)
                if not blacklist:
                    await asyncio.gather(
                        Blacklist.create(ip=ip, updated=updated, reason=reason, path=path),
                        send_message_alert(message=f'[*] Blocked IP: {ip} - Reason: {reason} - PATH: {path}')
                    )
                    log_debug('blocked ip', extra={'ip': ip, 'reason': reason})
        else:
            await cls.create(ip=ip, count=1, updated=updated, path=path)
