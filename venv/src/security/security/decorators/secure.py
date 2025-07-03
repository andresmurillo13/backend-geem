from datetime import datetime, timedelta

from starlette.responses import UJSONResponse

from security.controllers import IpRequest
from security.models import Blacklist, BlacklistAlert
from security.utils import ReasonEnum


def secure(reason=ReasonEnum.many_requests.value):
    def vd(f):
        async def wrapper(request, **kwargs):
            host, port = request.client
            ip_request = IpRequest()
            ip_request.set_ip(ip=host)
            now = datetime.today() - timedelta(hours=24)
            blacklist = await Blacklist.get_or_none(ip=host, updated={'$gte': now})
            if blacklist:
                if blacklist.reason == ReasonEnum.brute_force.value:
                    return UJSONResponse({'ok': False, 'message': 'invalid password'})
                else:
                    return UJSONResponse({'ok': False, 'message': 'Las credenciales de autenticación no se proveyeron.'})
            await BlacklistAlert.register_alert(ip=host, reason=reason, path=request.url.path)
            return await f(request, **kwargs)
        return wrapper
    return vd
