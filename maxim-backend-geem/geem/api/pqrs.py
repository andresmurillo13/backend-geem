from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required, login_notrequired

from geem.api.odm import CreatePqrsODM, DatePqrsODM, RespPqrsODM, CreatePqrsIntODM, GetPqrsUser, GetPqrsResp, ClosePqrsODM
from geem.controllers import Pqrs
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_pqrs = Starlette()


@app_pqrs.route(path='/createpqrs', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@validate(CreatePqrsODM)
async def createpqrs(request):
    data: dict = await request.json()
    res = await Pqrs(pqrstype=data.get('pqrstype'), claimanttype=data.get('claimanttype'), areas=data.get('areas'),
                    first_name=data.get('first_name'), last_name=data.get('last_name'),
                    type_person=data.get('type_person'), type_document=data.get('type_document'), num_document=data.get('num_document'),
                    email=data.get('email'), address=data.get('address'), country=data.get('country'),
                    city=data.get('city'), state=data.get('state'), phone=data.get('phone'),
                    ext=data.get('ext'), phone2=data.get('phone2'), ext2=data.get('ext2'),
                    action=data.get('action'),
                    message=data.get('message'), site=data.get('site'), form=data.get('form'), psnc=data.get('psnc'), locations=data.get('locations')
                    ).createPqrs()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una pqrs externa'})

@app_pqrs.route(path='/createpqrsint', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreatePqrsIntODM)
async def create_pqrs_internal(request):
    data: dict = await request.json()
    res = await Pqrs(pqrstype=data.get('pqrstype'), claimanttype=data.get('claimanttype'), areas=data.get('areas'),
                    action=data.get('action'), simaf=data.get('simaf'), companies=data.get('companies'),
                    message=data.get('message'), site=data.get('site'), form=data.get('form'), psnc=data.get('psnc'),
                    usr=request.user_id, company=request.company_id, locations=data.get('locations')).createPqrsInt()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una pqrs interna'})

@app_pqrs.route(path='/getpqrs/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpqrs(request):
    res = await Pqrs(id=request.path_params.get('id')).getPqrs()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            userc_name = ""
            if r.user:
                userc = r.user.id
                userc_name = r.user.first_name + " " + r.user.last_name
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
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
            companiesname = ""
            if r.companies.id:
                companiesname = r.companies.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
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
    return UJSONResponse({'message': 'Acción tramitada para consulta de una pqrs', 'result': pqrs})

@app_pqrs.route(path='/changecreated', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DatePqrsODM)
async def changecreated(request):
    data: dict = await request.json()
    res = await Pqrs(id=data.get('id'), created=data.get('created'),
                    usr=request.user_id, company=request.company_id).ChangeCreatedPqrs()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha de creacion de una pqrs'})

@app_pqrs.route(path='/changeresp', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(RespPqrsODM)
async def changeresp(request):
    data: dict = await request.json()
    res = await Pqrs(id=data.get('id'), user=data.get('user'),
                    usr=request.user_id, company=request.company_id).ChangeRespPqrs()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar el responsable de una pqrs'})

@app_pqrs.route(path='/pendpqrs/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendpqrs(request):
    res = await Pqrs(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).PendPqrs()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente una pqrs'})

@app_pqrs.route(path='/closepqrs', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(ClosePqrsODM)
async def closepqrs(request):
    data: dict = await request.json()
    res = await Pqrs(id=data.get('id'), obs_final=data.get('obs_final'),
                    usr=request.user_id, company=request.company_id).ClosePqrs()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada una pqrs'})

@app_pqrs.route(path='/deletepqrs', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(ClosePqrsODM)
async def deletepqrs(request):
    data: dict = await request.json()
    res = await Pqrs(id=data.get('id'), obs_final=data.get('obs_final'),
                    usr=request.user_id, company=request.company_id).DeletePqrs()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular una pqrs'})

@app_pqrs.route(path='/getpqrsactivities/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPqrsUser)
async def getpqrsactivities(request):
    data: dict = await request.json()
    res = await Pqrs(user=data.get('user'), page=request.path_params.get('page'),
                     form=data.get('form'), pqrstype=data.get('type'), key=data.get('key'),
                     status=data.get('status')).GetPqrsActivities()
    pqrs = []
    if res:
        for r in res[0]:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar actividades por usuario', 'result': pqrs, 'pages': res[1]})

@app_pqrs.route(path='/getpqrsuser/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPqrsUser)
async def getpqrsuser(request):
    data: dict = await request.json()
    res = await Pqrs(user=data.get('user'), page=request.path_params.get('page'),
                     key=data.get('key'), status=data.get('status')).GetPqrsUser()
    pqrs = []
    if res:
        for r in res[0]:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs por usuario', 'result': pqrs, 'pages': res[1]})

@app_pqrs.route(path='/getpqrscontroller/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPqrsResp)
async def getpqrcontroller(request):
    data: dict = await request.json()
    res = await Pqrs(page=request.path_params.get('page'),
                     form=data.get('form'), pqrstype=data.get('type'), key=data.get('key')
                     ).GetPqrsController()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs por controller', 'result': pqrs})

@app_pqrs.route(path='/getpqrsresp/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetPqrsResp)
async def getpqrsresp(request):
    data: dict = await request.json()
    res = await Pqrs(user_resp=data.get('user'), page=request.path_params.get('page'),
                     form=data.get('form'), pqrstype=data.get('type'), key=data.get('key')
                     ).GetPqrsResp()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs por responsable', 'result': pqrs})

@app_pqrs.route(path='/iscontroller/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscontroller(request):
    res = await Pqrs(user=request.path_params.get('user')).IsController()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es controller'})

@app_pqrs.route(path='/isresp/{user}/{pqrs}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscontroller(request):
    res = await Pqrs(user=request.path_params.get('user'), pqrs=request.path_params.get('pqrs')).IsResp()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es responsable de una pqrs.'})

@app_pqrs.route(path='/iscreator/{user}/{pqrs}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def iscreator(request):
    res = await Pqrs(user=request.path_params.get('user'), pqrs=request.path_params.get('pqrs')).IsCreator()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para saber si un usuario es creador de una pqrs.'})

@app_pqrs.route(path='/getpqrsresppend/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpqrsresppend(request):
    res = await Pqrs(user_resp=request.path_params.get('user')).GetPqrsRespPend()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs pendientes por responsable', 'result': pqrs})

@app_pqrs.route(path='/getpqrscontrollerpend/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpqrscontrollerpend(request):
    res = await Pqrs(user_boss=request.path_params.get('user')).GetPqrsControllerPend()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs pendientes por controller', 'result': pqrs})

@app_pqrs.route(path='/getpqrscontrollerasign/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getpqrscontrollerasign(request):
    res = await Pqrs(user_boss=request.path_params.get('user')).GetPqrsControllerAsign()
    pqrs = []
    if res:
        for r in res:
            clatype = ""
            claname = ""
            if r.claimanttype:
                clatype = r.claimanttype.id
                claname = r.claimanttype.name
            userc = ""
            if r.user:
                userc = r.user.id
            userr = ""
            if r.user_resp:
                userr = r.user_resp.id
            close = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            loca_id = ""
            loca_name = ""
            if r.locations:
                loca_id = r.locations.id
                loca_name = r.locations.name
            pqrs.append({
                'id': r.id,
                'pqrstype': r.pqrstype.id,
                'pqrstype_name': r.pqrstype.name,
                'claimanttype': clatype,
                "claimanttype_name": claname,
                'areas': r.areas.id,
                'areas_name': r.areas.name,
                'user_created': userc,
                'companies': r.companies.id,
                'user_resp': userr,
                'user_boss': r.user_boss.id,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'status': r.status,
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
                'obs_final': r.obs_final,
                'message': r.message,
                'action': r.action,
                'site': r.site,
                'form': r.form,
                'psnc': r.psnc,
                'locations_id': loca_id,
                'locations_name': loca_name
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar pqrs pendientes sin asignar responsable', 'result': pqrs})
