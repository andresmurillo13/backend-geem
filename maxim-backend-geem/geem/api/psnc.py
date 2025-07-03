from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required, login_notrequired

from geem.api.odm import CreatePsncODM, DatePsncODM, RespPsncODM, GetPsncResp, GetPsncUser, ClosePsncODM, CreatePsncODMExt
from geem.controllers import Psnc
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_psnc = Starlette()


@app_psnc.route(path='/createpsnc', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreatePsncODM)
async def createpsnc(request):
    data: dict = await request.json()
    res = await Psnc(areas=data.get('areas'), typepsnc=data.get('typepsnc'), event_date=data.get('event_date'),
                     created=data.get('created'), action=data.get('action'), companies=data.get('companies'),
                     message=data.get('message'), site=data.get('site'), simaf=data.get('simaf'),
                     usr=request.user_id, company=request.company_id, locations=data.get('locations')).createPsnc()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un psnc'})

@app_psnc.route(path='/createpsncext', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@validate(CreatePsncODMExt)
async def createpsnc(request):
    data: dict = await request.json()
    res = await Psnc(pqrstype=data.get('pqrstype'), claimanttype=data.get('claimanttype'), areas=data.get('areas'),
                     first_name=data.get('first_name'), last_name=data.get('last_name'),
                     type_person=data.get('type_person'), event_date=data.get('event_date'),
                     type_document=data.get('type_document'), num_document=data.get('num_document'),
                     email=data.get('email'), address=data.get('address'), country=data.get('country'),
                     city=data.get('city'), state=data.get('state'), phone=data.get('phone'),
                     ext=data.get('ext'), phone2=data.get('phone2'), ext2=data.get('ext2'),
                     action=data.get('action'), message=data.get('message'), site=data.get('site'),
                     form=data.get('form'), psnc=data.get('psnc'), typepsnc=data.get('typepsnc'), locations=data.get('locations')).createPsncExt()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un psnc externo'})

@app_psnc.route(path='/getpsnc/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpsnc(request):
    res = await Psnc(id=request.path_params.get('id')).getPsnc()
    psnc = []
    if res:
        for r in res:
            userc = ""
            userc_name = ""
            if r.user.id:
                userc = r.user.id
                userc_name = r.user.first_name + " " + r.user.last_name
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            companiesname = ""
            if r.companies.id:
                companiesname = r.companies.name
            name = ""
            email = ""
            tlf = ""
            address = ""
            country = ""
            state = ""
            city = ""
            if r.first_name == None:
                name = r.user.first_name
                email = r.user.email
                tlf = r.user.phone
                address = "Km 4 Vía Palermo Bodega B03 Parque Industrial el Viso"
                country = "Colombia"
                state = "Huila"
                city = "Neiva"
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'user_created_name': userc_name,
                'companies': r.companies.id,
                'companiesname': companiesname,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'first_name': r.first_name,
                'last_name': r.last_name,
                'type_person': r.type_person,
                'type_document': r.type_document,
                'num_document': r.num_document,
                'email': r.email,
                'address': r.address,
                'country': r.country,
                'city': r.city,
                'state': r.state,
                'phone': r.phone,
                'ext': r.ext,
                'ext2': r.ext2,
                'phone2': r.phone2,
                'score': r.score,
                'usr_name': name,
                'usr_email': email,
                'usr_tlf': tlf,
                'usr_address': address,
                'usr_country': country,
                'usr_state': state,
                'usr_city': city,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de un psnc', 'result': psnc})

@app_psnc.route(path='/changecreated', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DatePsncODM)
async def changecreated(request):
    data: dict = await request.json()
    res = await Psnc(id=data.get('id'), created=data.get('created'),
                    usr=request.user_id, company=request.company_id).ChangeCreatedPsnc()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha de creacion de un psnc'})

@app_psnc.route(path='/changeresp', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(RespPsncODM)
async def changeresp(request):
    data: dict = await request.json()
    res = await Psnc(id=data.get('id'), user=data.get('user'),
                    usr=request.user_id, company=request.company_id).ChangeRespPsnc()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar el responsable de un psnc'})

@app_psnc.route(path='/pendpsnc/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendpsnc(request):
    res = await Psnc(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).PendPsnc()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente un psnc'})

@app_psnc.route(path='/closepsnc', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(ClosePsncODM)
async def closepsnc(request):
    data: dict = await request.json()
    res = await Psnc(id=data.get('id'), obs_final=data.get('obs_final'),
                    usr=request.user_id, company=request.company_id).ClosePsnc()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada un psnc'})

@app_psnc.route(path='/deletepsnc', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(ClosePsncODM)
async def deletepsnc(request):
    data: dict = await request.json()
    res = await Psnc(id=data.get('id'), obs_final=data.get('obs_final'),
                    usr=request.user_id, company=request.company_id).DeletePsnc()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular un psnc'})

@app_psnc.route(path='/getpsncactivities/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncUser)
async def getpsncactivities(request):
    data: dict = await request.json()
    res = await Psnc(user=data.get('user'), page=request.path_params.get('page'),
                     form=data.get('form'), typepsnc=data.get('type'), key=data.get('key'),
                     status=data.get('status')).GetPsncActivities()
    psnc = []
    if res:
        for r in res[0]:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar actividades por usuario en PSNC', 'result': psnc, 'pages': res[1]})


@app_psnc.route(path='/getpsncuser/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncUser)
async def getpsncuser(request):
    data: dict = await request.json()
    res = await Psnc(user=data.get('user'), page=request.path_params.get('page'),
                     key=data.get('key'), status=data.get('status'), typepsnc=data.get('type')).GetPsncUser()
    psnc = []
    if res:
        for r in res[0]:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc por usuario', 'result': psnc, 'pages': res[1]})

@app_psnc.route(path='/getpsnccontroller/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncResp)
async def getpsnccontroller(request):
    data: dict = await request.json()
    res = await Psnc(page=request.path_params.get('page'), typepsnc=data.get('type'),
                     status=data.get('status'), key=data.get('key')
                     ).GetPsncController()
    psnc = []
    if res:
        for r in res:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc por controller', 'result': psnc})

@app_psnc.route(path='/getpsncresp/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPsncResp)
async def getpsncresp(request):
    data: dict = await request.json()
    res = await Psnc(user_resp=data.get('user'), page=request.path_params.get('page'),
                     status=data.get('status'), key=data.get('key'), typepsnc=data.get('type')
                     ).GetPsncResp()
    psnc = []
    if res:
        for r in res:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc por responsable', 'result': psnc})

@app_psnc.route(path='/iscontroller/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscontroller(request):
    res = await Psnc(user=request.path_params.get('user')).IsController()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es controller'})

@app_psnc.route(path='/isresp/{user}/{psnc}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscontroller(request):
    res = await Psnc(user=request.path_params.get('user'), psnc=request.path_params.get('psnc')).IsResp()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es responsable de un psnc.'})

@app_psnc.route(path='/iscreator/{user}/{psnc}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscreator(request):
    res = await Psnc(user=request.path_params.get('user'), psnc=request.path_params.get('psnc')).IsCreator()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es creador de un psnc.'})

@app_psnc.route(path='/getpsncresppend/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpsncresppend(request):
    res = await Psnc(user_resp=request.path_params.get('user')).GetPsncRespPend()
    psnc = []
    if res:
        for r in res:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc pendientes por responsable', 'result': psnc})

@app_psnc.route(path='/getpsnccontrollerpend/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpsnccontrollerpend(request):
    res = await Psnc(user_boss=request.path_params.get('user')).GetPsncControllerPend()
    psnc = []
    if res:
        for r in res:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc pendientes por controller', 'result': psnc})

@app_psnc.route(path='/getpsnccontrollerasign/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpsnccontrollerasign(request):
    res = await Psnc(user_boss=request.path_params.get('user')).GetPsncControllerAsign()
    psnc = []
    if res:
        for r in res:
            userc = ""
            if r.user.id:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            eventdate = ""
            if r.event_date:
                eventdate = r.event_date.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            psnc.append({
                'id': r.id,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'typepsnc': r.typepsnc,
                'event_date': eventdate,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar psnc pendientes sin asignar responsable', 'result': psnc})