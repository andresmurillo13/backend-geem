from functools import wraps
from json import JSONDecodeError

from marshmallow import ValidationError
from starlette.responses import JSONResponse


def validate(cls):
    def vd(f):
        @wraps(f)
        async def wrapper(request, **kwargs):
            data = request.path_params
            if request.method == 'POST':
                try:
                    data.update(await request.json())
                except JSONDecodeError:
                    return JSONResponse({'ok': False, 'errors': {},
                                         'message': 'No es formato JSON'})
            data = {i: data[i] for i in data if data[i]}
            schema = cls()
            try:
                schema.load(data)
            except ValidationError as error:
                return JSONResponse({'ok': False, 'errors': error.messages,
                                     'message': ''})
            return await f(request, **kwargs)
        return wrapper
    return vd
