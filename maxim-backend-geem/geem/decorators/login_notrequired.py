from datetime import datetime, timedelta
from functools import wraps

from starlette.responses import JSONResponse

from geem.models import ModelUser, ModelCompanies


def login_notrequired():
    def vd(f):
        @wraps(f)
        async def wrapper(request, **kwargs):
            authorization: str = request.headers.get('authorization')
            if authorization and 'Bearer' in authorization:
                token = authorization.replace('Bearer ', '')
                user = await ModelUser.get_or_none(token=token, is_active=True)
                if user:
                    if user.token_expired.timestamp() > datetime.utcnow().timestamp():
                        user.token_expired = datetime.utcnow() + timedelta(days=1)
                        await user.save()
                        request.user_id = user.id
                        company: ModelCompanies = await user.company
                        request.company_id = company.id
                        return await f(request, **kwargs)
                return JSONResponse({'ok': False, 'errors': {},
                                 'message': 'Las credenciales de autenticación no se proveyeron bien.'})
            request.user_id = None
            request.company_id = None
            return await f(request, **kwargs)
        return wrapper
    return vd
