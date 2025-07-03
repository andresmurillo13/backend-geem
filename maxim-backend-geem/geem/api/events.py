from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateEventODM, UpdateEventODM, UseEventODM, GetEventUser, CloseEventODM
from geem.controllers import Events
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_events = Starlette()


@app_events.route(path='/createevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateEventODM)
async def createevent(request):
    data: dict = await request.json()
    res = await Events(description=data.get('description'), reporter=data.get('reporter'), date=data.get('date'),
                        cost=data.get('cost'), event_type=data.get('event_type'), property_damage=data.get('property_damage'),
                        usr=request.user_id, company=request.company_id).createEvent()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un evento'})

@app_events.route(path='/updateevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdateEventODM)
async def updateevent(request):
    data: dict = await request.json()
    res = await Events(description=data.get('description'), reporter=data.get('reporter'), date=data.get('date'),
                     cost=data.get('cost'), event_type=data.get('event_type'),
                     id=data.get('id'), effectiv=data.get('effectiv'), status=data.get('status'),
                     date_close=data.get('date_close'), property_damage=data.get('property_damage'),
                     usr=request.user_id, company=request.company_id
                     ).updateEvent()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para la actualización de un evento'})

@app_events.route(path='/getevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getevent(request):
    res = await Events(id=request.path_params.get('id')).getEvent()
    event = []
    if res:
        for r in res:
            close = ""
            update = ""
            dclose = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.date_close:
                dclose = r.date_close.strftime('%Y/%m/%d')
            event.append({
                'id': r.id,
                'description': r.description,
                'date': r.date.strftime('%Y/%m/%d'),
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'cost': r.cost,
                'user_id': r.user.id,
                'user_name': r.user.first_name,
                'user_lastname': r.user.last_name,
                'event_type_id': r.eventtype.id,
                'event_type': r.eventtype.description,
                'status': r.status,
                'reporter': r.reporter,
                'date_close': dclose,
                'property_damage': r.property_damage,
                'b_close': r.close,
                'b_update': r.update,
                'b_delete': r.delete,
                'b_activate': r.activate
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de un evento', 'result': event})

@app_events.route(path='/geteventuser/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetEventUser)
async def geteventuser(request):
    data: dict = await request.json()
    res = await Events(page=request.path_params.get('page'), status=data.get('status'), key=data.get('key'), usr=request.user_id
                     ).getEventUser()
    events = []
    if res:
        for r in res[0]:
            close = ""
            update = ""
            dclose = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.date_close:
                update = r.date_close.strftime('%Y/%m/%d')
            events.append({
                'id': r.id,
                'description': r.description,
                'date': r.date.strftime('%Y/%m/%d'),
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'cost': r.cost,
                'user_id': r.user.id,
                'user_name': r.user.first_name,
                'user_lastname': r.user.last_name,
                'event_type_id': r.eventtype.id,
                'event_type': r.eventtype.description,
                'status': r.status,
                'reporter': r.reporter,
                'date_close': dclose,
                'property_damage': r.property_damage
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar los eventos generadas por un usuario', 'result': events, 'pages': res[1]})

@app_events.route(path='/getevents/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetEventUser)
async def getevents(request):
    data: dict = await request.json()
    res = await Events(page=request.path_params.get('page'), status=data.get('status'), key=data.get('key')
                     ).getEvents()
    events = []
    if res:
        for r in res[0]:
            close = ""
            update = ""
            dclose = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.date_close:
                update = r.date_close.strftime('%Y/%m/%d')
            events.append({
                'id': r.id,
                'description': r.description,
                'date': r.date.strftime('%Y/%m/%d'),
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'cost': r.cost,
                'user_id': r.user.id,
                'user_name': r.user.first_name,
                'user_lastname': r.user.last_name,
                'event_type_id': r.eventtype.id,
                'event_type': r.eventtype.description,
                'status': r.status,
                'reporter': r.reporter,
                'date_close': dclose,
                'property_damage': r.property_damage
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar los eventos', 'result': events, 'pages': res[1]})

@app_events.route(path='/pendevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendevent(request):
    res = await Events(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).pendEvent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente un evento'})

@app_events.route(path='/closeevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CloseEventODM)
async def closeevent(request):
    data: dict = await request.json()
    res = await Events(id=data.get('id'), effectiv=data.get('effectiv'), date_close=data.get('date_close'),
                    usr=request.user_id, company=request.company_id).closeEvent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrado un evento'})

@app_events.route(path='/deleteevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deleteevent(request):
    res = await Events(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).deleteEvent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular un evento'})