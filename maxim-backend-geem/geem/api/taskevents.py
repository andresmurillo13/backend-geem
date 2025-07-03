from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateTaskeventsODM, UseTaskeventsODM, UpdateTaskeventsODM, GetTaskeventsUser, CloseTaskeventsODM, DeliverTaskeventsODM
from geem.controllers import Taskevents
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_taskevents = Starlette()


@app_taskevents.route(path='/createtaskevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateTaskeventsODM)
async def createtaskevent(request):
    data: dict = await request.json()
    res = await Taskevents(description=data.get('description'), user=data.get('user'), action_task=data.get('action_task'),
                            finding=data.get('finding'), areas=data.get('areas'), created_e=data.get('created_e'),
                            usr=request.user_id, company=request.company_id).createTaskevent()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una tarea de hallazgo'})

@app_taskevents.route(path='/updatetaskevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdateTaskeventsODM)
async def updatetaskevent(request):
    data: dict = await request.json()
    res = await Taskevents(description=data.get('description'), description_close=data.get('description_close'),
                            description_evidence=data.get('description_evidence'), user=data.get('user'),
                            action_task=data.get('action_task'), finding=data.get('finding'),
                            created_e=data.get('created_e'), closed_e=data.get('closed_e'), areas=data.get('areas'),
                            effectiv=data.get('effectiv'), status=data.get('status'), id=data.get("id"),
                            usr=request.user_id, company=request.company_id
                            ).updateTaskevent()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para la actualización de una tarea de hallazgo'})

@app_taskevents.route(path='/gettaskevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskevent(request):
    res = await Taskevents(id=request.path_params.get('id'), usr=request.user_id).getTaskevent()
    taskevent = []
    if res:
        for r in res:
            close = ""
            update = ""
            close_e = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.closed_e:
                close_e = r.closed_e.strftime('%Y/%m/%d')
            taskevent.append({
                'id': r.id,
                'description': r.description,
                'desccription_close': r.description_close,
                'description_evidence': r.description_evidence,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_task_id': r.actiontask.id,
                'action_task_desccription': r.actiontask.description,
                'finding_id': r.finding.id,
                'finding_description': r.finding.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'status': r.status,
                'created_e': r.created_e.strftime('%Y/%m/%d'),
                'closed_e': close_e,
                'b_close': r.close,
                'b_update': r.update,
                'b_delete': r.delete,
                'b_activate': r.activate,
                'b_delivery': r.delivery,
                'createblock': r.createblock,
                'deliverblock': r.deliverblock,
                'closeblock': r.closeblock
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una tarea de hallazgo', 'result': taskevent})

@app_taskevents.route(path='/gettaskeventsrespfinding/{finding}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetTaskeventsUser)
async def gettaskeventsresp(request):
    res = await Taskevents(finding=request.path_params.get('finding'), usr=request.user_id).getTaskeventsRespFinding()
    taskevents = []
    if res:
        for r in res:
            close = ""
            update = ""
            close_e = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.closed_e:
                close_e = r.closed_e.strftime('%Y/%m/%d')
            taskevents.append({
                'id': r.id,
                'description': r.description,
                'desccription_close': r.description_close,
                'description_evidence': r.description_evidence,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_task_id': r.actiontask.id,
                'action_task_desccription': r.actiontask.description,
                'finding_id': r.finding.id,
                'finding_description': r.finding.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'status': r.status,
                'created_e': r.created_e.strftime('%Y/%m/%d'),
                'closed_e': close_e,
                'b_close': r.close,
                'b_update': r.update,
                'b_delete': r.delete,
                'b_activate': r.activate,
                'b_delivery': r.delivery,
                'resp': r.resp
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar las tareas de hallazgos asigandas por hallazgo y usuario', 'result': taskevents})

@app_taskevents.route(path='/gettaskeventsresp/{page}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetTaskeventsUser)
async def gettaskeventsresp(request):
    res = await Taskevents(page=request.path_params.get('page'), usr=request.user_id).getTaskeventsResp()
    taskevents = []
    if res:
        for r in res[0]:
            close = ""
            update = ""
            close_e = ""
            created_e = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.closed_e:
                close_e = r.closed_e.strftime('%Y/%m/%d')
                if r.created_e:
                    created_e = r.created_e.strftime('%Y/%m/%d')
            taskevents.append({
                'id': r.id,
                'description': r.description,
                'desccription_close': r.description_close,
                'description_evidence': r.description_evidence,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_task_id': r.actiontask.id,
                'action_task_desccription': r.actiontask.description,
                'finding_id': r.finding.id,
                'event_id': r.finding.event.id,
                'finding_description': r.finding.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'status': r.status,
                'created_e': created_e,
                'closed_e': close_e
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar las tareas de hallazgos pendientes en general para un usuario', 'result': taskevents, 'pages': res[1]})

@app_taskevents.route(path='/gettaskeventsfinding/{finding}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(GetTaskeventsUser)
async def gettaskeventsfinding(request):
    res = await Taskevents(finding=request.path_params.get('finding')).getTaskeventsFinding()
    taskevents = []
    if res:
        for r in res:
            close = ""
            update = ""
            close_e = ""
            if r.closed:
                close = r.closed.strftime('%Y/%m/%d')
            if r.updated:
                update = r.updated.strftime('%Y/%m/%d')
            if r.closed_e:
                close_e = r.closed_e.strftime('%Y/%m/%d')
            taskevents.append({
                'id': r.id,
                'description': r.description,
                'desccription_close': r.description_close,
                'description_evidence': r.description_evidence,
                'created': r.created.strftime('%Y/%m/%d'),
                'closed': close,
                'updated': update,
                'effectiv': r.effectiv,
                'resp_id': r.user.id,
                'resp_name': r.user.first_name,
                'resp_lastname': r.user.last_name,
                'action_task_id': r.actiontask.id,
                'action_task_desccription': r.actiontask.description,
                'finding_id': r.finding.id,
                'finding_description': r.finding.description,
                'area_id': r.area.id,
                'area_name': r.area.name,
                'status': r.status,
                'created_e': r.created_e.strftime('%Y/%m/%d'),
                'closed_e': close_e,
                'b_close': r.close,
                'b_update': r.update,
                'b_delete': r.delete,
                'b_activate': r.activate,
                'b_delivery': r.delivery
            })
    return UJSONResponse({'message': 'Acción tramitada para consultar las tareas de hallazgos asigandas por hallazgo', 'result': taskevents})

@app_taskevents.route(path='/pendtaskevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendtaskevent(request):
    res = await Taskevents(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).pendTaskevent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente una tarea de hallazgo'})

@app_taskevents.route(path='/closetaskevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CloseTaskeventsODM)
async def closetaskevent(request):
    data: dict = await request.json()
    res = await Taskevents(effectiv=data.get('effectiv'), id=data.get("id"),
                    usr=request.user_id, company=request.company_id).closeTaskevent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada una tarea de hallazgo'})

@app_taskevents.route(path='/deletetaskevent/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deletetaskevent(request):
    res = await Taskevents(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).deleteTaskevent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para borrar una tarea de hallazgo'})

@app_taskevents.route(path='/delivertaskevent', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DeliverTaskeventsODM)
async def delivertaskevent(request):
    data: dict = await request.json()
    res = await Taskevents(id=data.get("id"), description_close=data.get('description_close'),
                           closed_e=data.get('closed_e'), description_evidence=data.get('description_evidence'),
                            usr=request.user_id, company=request.company_id).deliverTaskevent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para entregar una tarea de hallazgo'})