from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateFindingODM, UseFindingODM, GetFindingUser, UpdateFindingODM, DeliverFindingODM, CloseFindingODM
from geem.controllers import Findings
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_findings = Starlette()


@app_findings.route(path='/createfinding', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateFindingODM)
async def createfinding(request):
    data: dict = await request.json()
    res = await Findings(description=data.get('description'), correction=data.get('correction'), repeated=data.get('repeated'),
                         user=data.get('user'), action_type=data.get('action_type'), finding_type=data.get('finding_type'),
                        events=data.get('events'), locations=data.get('locations'), areas=data.get('areas'),
                        usr=request.user_id, company=request.company_id).createFinding()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un hallazgo'})

@app_findings.route(path='/updatefinding', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdateFindingODM)
async def updatefinding(request):
    data: dict = await request.json()
    res = await Findings(description=data.get('description'), correction=data.get('correction'), repeated=data.get('repeated'),
                         user=data.get('user'), action_type=data.get('action_type'), finding_type=data.get('finding_type'),
                         events=data.get('events'), locations=data.get('locations'), areas=data.get('areas'), id=data.get("id"),
                         effectiv=data.get('effectiv'), status=data.get('status'),
                         usr=request.user_id, company=request.company_id
                        ).updateFinding()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para la actualización de un hallazgo'})

@app_findings.route(path='/getfinding/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getfinding(request):
    res = await Findings(id=request.path_params.get('id'), usr=request.user_id).getFinding()
    finding = []
    if res:
        for r in res:
            close = ""
            update = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            finding.append({
                'id': r.id,
                'description': r.description,
                'correction': r.correction,
                'repeated': r.repeated,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_type_id': r.actiontype.id,
                'action_type_desccription': r.actiontype.description,
                'finding_type_id': r.findingtype.id,
                'finding_type_description': r.findingtype.description,
                'event_id': r.event.id,
                'event_description': r.event.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'location_id': r.location.id,
                'location_name': r.location.name,
                'status': r.status,
                'b_close': r.close,
                'b_update': r.update,
                'b_delete': r.delete,
                'b_activate': r.activate,
                'b_delivery': r.delivery,
                'createblock': r.createblock,
                'deliverblock': r.deliverblock,
                'closeblock': r.closeblock
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de un hallazgo', 'result': finding})

@app_findings.route(path='/getfindingsresp/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetFindingUser)
async def getfindingsresp(request):
    data: dict = await request.json()
    res = await Findings(page=request.path_params.get('page'), status=data.get('status'), key=data.get('key'), usr=request.user_id
                     ).getFindingsResp()
    findings = []
    if res:
        for r in res[0]:
            close = ""
            update = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            findings.append({
                'id': r.id,
                'description': r.description,
                'correction': r.correction,
                'repeated': r.repeated,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_type_id': r.actiontype.id,
                'action_type_desccription': r.actiontype.description,
                'finding_type_id': r.findingtype.id,
                'finding_type_description': r.findingtype.description,
                'event_id': r.event.id,
                'event_description': r.event.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'location_id': r.location.id,
                'location_name': r.location.name,
                'status': r.status
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar los hallazgos asigandos como usuarios responsables', 'result': findings, 'pages': res[1]})

@app_findings.route(path='/getfindingsuser/{page}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetFindingUser)
async def getfindingsuser(request):
    data: dict = await request.json()
    res = await Findings(page=request.path_params.get('page'), status=data.get('status'), key=data.get('key'), usr=request.user_id
                     ).getFindingsUser()
    findings = []
    if res:
        for r in res[0]:
            close = ""
            update = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            findings.append({
                'id': r.id,
                'description': r.description,
                'correction': r.correction,
                'repeated': r.repeated,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_type_id': r.actiontype.id,
                'action_type_desccription': r.actiontype.description,
                'finding_type_id': r.findingtype.id,
                'finding_type_description': r.findingtype.description,
                'event_id': r.event.id,
                'event_description': r.event.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'location_id': r.location.id,
                'location_name': r.location.name,
                'status': r.status
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar los hallazgos asigandos como usuarios responsables', 'result': findings, 'pages': res[1]})

@app_findings.route(path='/getfindingsevent/{event}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetFindingUser)
async def getfindingsresp(request):
    res = await Findings(events=request.path_params.get('event')).getFindingsEvent()
    findings = []
    if res:
        for r in res:
            close = ""
            update = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            findings.append({
                'id': r.id,
                'description': r.description,
                'correction': r.correction,
                'repeated': r.repeated,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_type_id': r.actiontype.id,
                'action_type_desccription': r.actiontype.description,
                'finding_type_id': r.findingtype.id,
                'finding_type_description': r.findingtype.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'location_id': r.location.id,
                'location_name': r.location.name,
                'status': r.status
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar los hallazgos por evento', 'result': findings})

@app_findings.route(path='/pendfinding/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendfinding(request):
    res = await Findings(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).pendFinding()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente un hallazgo'})

@app_findings.route(path='/closefinding', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CloseFindingODM)
async def closefinding(request):
    data: dict = await request.json()
    res = await Findings(id=data.get('id'), effectiv=data.get('effectiv'),
                    usr=request.user_id, company=request.company_id).closeFinding()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrado un hallazgo'})

@app_findings.route(path='/deletefinding/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deletefinding(request):
    res = await Findings(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).deleteFinding()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para borrar un hallazgo'})

@app_findings.route(path='/deliverfinding', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DeliverFindingODM)
async def deliverfinding(request):
    data: dict = await request.json()
    res = await Findings(id=data.get('id'), correction=data.get('correction'),
                    usr=request.user_id, company=request.company_id).deliverFinding()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para entregar un hallazgo'})