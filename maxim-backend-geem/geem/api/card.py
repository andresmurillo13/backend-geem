from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required, login_notrequired

from geem.api.odm import CreatePsncODM, DateCardODM, RespCardODM, CreateCardODM, GetPsncResp, CloseCardODM
from geem.controllers import Psnc
from geem.controllers import Card
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_card = Starlette()


@app_card.route(path='/createcard', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateCardODM)
async def createcard(request):
    data: dict = await request.json()
    res = await Card(type=data.get('type'), event_date=data.get('event_date'), document=data.get('document'),
                     first_name=data.get('first_name'), last_name=data.get('last_name'),
                     compa=data.get('company'), position=data.get('position'),
                     obs=data.get('obs'), action=data.get('action'), close=data.get('close'),
                     site=data.get('site'), user_obs=data.get('user_obs'), items=data.get('items'), simaf=data.get('simaf'),
                    usr=request.user_id, company=request.company_id, locations=data.get('locations'),
                     companies=data.get('companies'), zone=data.get('zone')).createCard()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una tarjeta'})

@app_card.route(path='/getcard/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getcard(request):
    res = await Card(id=request.path_params.get('id')).getCard()
    card = []
    if res:
        for r in res:
            usero_id = ""
            usero_name = ""
            usero_surname = ""
            usero_email = ""
            if r.user_obs:
                usero_id = r.user_obs.id
                usero_name = r.user_obs.first_name
                usero_surname = r.user_obs.last_name
                usero_email = r.user_obs.email
            userr_id = ""
            userr_name = ""
            userr_surname = ""
            userr_email = ""
            if r.user_resp:
                userr_id = r.user_resp.id
                userr_name = r.user_resp.first_name
                userr_surname = r.user_resp.last_name
                userr_email = r.user_resp.email
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            it = []
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            companiesid = ""
            companiesname = ""
            if r.companies:
                companiesid = r.companies.id
                companiesname = r.companies.name
            areasid = ""
            areasname = ""
            if r.areas:
                areasid = r.areas.id
                areasname = r.areas.name
            for i in r.items:
                it.append({
                    'id': i.id,
                    'level': i.level,
                    'level2': i.level2,
                    'description': i.description
                })
            card.append({
                'id': r.id,
                'type': r.type,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'document': r.document,
                'first_name': r.first_name,
                'last_name': r.last_name,
                'company': r.company,
                'position': r.position,
                'site': r.site,
                'obs': r.obs,
                'action': r.action,
                'close': r.close,
                'status': r.status,
                'user_created_id': r.user.id,
                'user_created_name': r.user.first_name,
                'user_created_surname': r.user.last_name,
                'user_created_email': r.user.email,
                'user_obs_id': usero_id,
                'user_obs_name': usero_name,
                'user_obs_surname': usero_surname,
                'user_obs_email': usero_email,
                'user_resp_id': userr_id,
                'user_resp_name': userr_name,
                'user_resp_surname': userr_surname,
                'user_resp_email': userr_email,
                'user_boss_id': r.user_boss_id,
                'locations_id': loca_id,
                'locations_name': loca_name,
                'items': it,
                'companies_id': companiesid,
                'companies_name': companiesname,
                'areas_id': areasid,
                'areas_name': areasname,
                'zone': r.zone
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una tarjeta', 'result': card})

@app_card.route(path='/changecreated', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DateCardODM)
async def changecreated(request):
    data: dict = await request.json()
    res = await Card(id=data.get('id'), created=data.get('created'),
                    usr=request.user_id, company=request.company_id).ChangeCreatedCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha de creacion de una tarjeta'})

@app_card.route(path='/changeresp', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(RespCardODM)
async def changeresp(request):
    data: dict = await request.json()
    res = await Card(id=data.get('id'), user=data.get('user'), areas=data.get('areas'),
                    usr=request.user_id, company=request.company_id).ChangeRespCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar el responsable de una tarjeta'})

@app_card.route(path='/pendcard/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendpsnc(request):
    res = await Card(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).PendCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente una tarjeta'})

@app_card.route(path='/closecard', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CloseCardODM)
async def closepsnc(request):
    data: dict = await request.json()
    res = await Card(id=data.get('id'), close=data.get('close'),
                    usr=request.user_id, company=request.company_id).CloseCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada una tarjeta'})

@app_card.route(path='/deletecard', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CloseCardODM)
async def deletepsnc(request):
    data: dict = await request.json()
    res = await Card(id=data.get('id'), close=data.get('close'),
                    usr=request.user_id, company=request.company_id).DeleteCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular uan tarjeta'})

@app_card.route(path='/getitemslevel/{level}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getitemslevel(request):
    res = await Card(level=request.path_params.get('level'),
                    usr=request.user_id, company=request.company_id).getLevelItems()
    items = []
    if res:
        for r in res:
            items.append({
                'id': r.id,
                'description': r.description,
                'level': r.level,
                'level2': r.level2,
                'audit': r.audit,
                'version': r.version_id,
                'version_des': r.version.description
            })
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para traer los items seleccionados por nivel', 'result': items})

@app_card.route(path='/getobsuser/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getobsuser(request):
    res = await Card(user=request.path_params.get('user')).getObsUser()
    select = []
    if res:
        for r in res:
            select.append({
                'id': r.id,
                'name': r.first_name,
                'surname': r.last_name
            })
        select.append({
            'id': 10000,
            'name': "Persona",
            'surname': "Externa"
        })
    return UJSONResponse({'message': 'Acción tramitada para traer el select de observadores por tarjeta', 'result': select})

@app_card.route(path='/getcarduser/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncResp)
async def getcarduser(request):
    data: dict = await request.json()
    res = await Card(page=request.path_params.get('page'), user=data.get('user'),
                     status=data.get('status'), key=data.get('key')
                     ).GetCardUser()
    cards = []
    if res:
        for r in res[0]:
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            cards.append({
                'id': r.id,
                'obs': r.obs,
                'action': r.action,
                'created': r.created.strftime('%Y/%m/%d'),
                'site': r.site,
                'status': r.status,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar la tarjetas generadas por un usuario', 'result': cards, 'pages': res[1]})

@app_card.route(path='/getcardactivities/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncResp)
async def getcardactivities(request):
    data: dict = await request.json()
    res = await Card(page=request.path_params.get('page'), user=data.get('user'),
                     status=data.get('status'), key=data.get('key')
                     ).GetCardActivities()
    cards = []
    if res:
        for r in res:
            cards = []
            if res:
                for r in res[0]:
                    loca_id = ""
                    loca_name = ""
                    if r.locations:
                        loca_id = r.locations.id
                        loca_name = r.locations.name
                    cards.append({
                        'id': r.id,
                        'obs': r.obs,
                        'action': r.action,
                        'created': r.created.strftime('%Y/%m/%d'),
                        'site': r.site,
                        'status': r.status,
                        'locations_id': loca_id,
                        'locations_name': loca_name
                    })
    return UJSONResponse({'message': 'Acción tramitada para actividades de tarjestas por usuario', 'result': cards, 'pages': res[1]})

@app_card.route(path='/iscontroller/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscontroller(request):
    res = await Card(user=request.path_params.get('user')).IsController()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es controller en una tarjeta'})

@app_card.route(path='/isresp/{user}/{card}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def isresp(request):
    res = await Card(user=request.path_params.get('user'), card=request.path_params.get('card')).IsResp()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es responsable de una tarjeta.'})

@app_card.route(path='/iscreator/{user}/{card}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscreator(request):
    res = await Card(user=request.path_params.get('user'), card=request.path_params.get('card')).IsCreator()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es creador de una tarjeta.'})


@app_card.route(path='/getcardactivities/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncResp)
async def getcardactivities(request):
    data: dict = await request.json()
    res = await Card(page=request.path_params.get('page'), user=data.get('user'),
                     status=data.get('status'), key=data.get('key')
                     ).GetCardActivities()
    cards = []
    if res:
        for r in res:
            cards = []
            if res:
                for r in res:
                    loca_id = ""
                    loca_name = ""
                    if r.locations:
                        loca_id = r.locations.id
                        loca_name = r.locations.name
                    cards.append({
                        'id': r.id,
                        'obs': r.obs,
                        'action': r.action,
                        'created': r.created.strftime('%Y/%m/%d'),
                        'site': r.site,
                        'status': r.status,
                        'locations_id': loca_id,
                        'locations_name': loca_name
                    })
    return UJSONResponse({'message': 'Acción tramitada para actividades de tarjestas por usuario', 'result': cards})
@app_card.route(path='/getcardpend/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getcardpend(request):
    res = await Card(user=request.path_params.get('user')).GetCardPend()
    cards = []
    if res:
        for r in res:
            cards = []
            if res:
                for r in res:
                    loca_id = ""
                    loca_name = ""
                    if r.locations:
                        loca_id = r.locations.id
                        loca_name = r.locations.name
                    cards.append({
                        'id': r.id,
                        'obs': r.obs,
                        'action': r.action,
                        'created': r.created.strftime('%Y/%m/%d'),
                        'site': r.site,
                        'status': r.status,
                        'locations_id': loca_id,
                        'locations_name': loca_name
                    })
    return UJSONResponse({'message': 'Acción tramitada para consultar tarjetas pendientes por usuario', 'result': cards})

@app_card.route(path='/getcardcontrollerasign/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getcardcontrollerasign(request):
    res = await Card(user_boss=request.path_params.get('user')).GetCardControllerAsign()
    cards = []
    if res:
        for r in res:
            cards = []
            if res:
                for r in res:
                    loca_id = ""
                    loca_name = ""
                    if r.locations:
                        loca_id = r.locations.id
                        loca_name = r.locations.name
                    cards.append({
                        'id': r.id,
                        'obs': r.obs,
                        'action': r.action,
                        'created': r.created.strftime('%Y/%m/%d'),
                        'site': r.site,
                        'status': r.status,
                        'locations_id': loca_id,
                        'locations_name': loca_name
                    })
    return UJSONResponse({'message': 'Acción tramitada para consultar tarjetas pendientes sin asignar responsable', 'result': cards})