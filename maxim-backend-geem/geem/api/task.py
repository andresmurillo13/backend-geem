from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateTaskODM, UseTaskODM, DateTaskODM, UpdateObsODM, UserTaskODM, DeliverObsODM
from geem.controllers import Task
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_task = Starlette()


@app_task.route(path='/createtask', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateTaskODM)
async def createtask(request):
    data: dict = await request.json()
    res = await Task(pqrs=data.get('pqrs'), user_resp=data.get('user_resp'), description=data.get('description'),
                    status=data.get('status'), obs=data.get('obs'), created=data.get('created'),
                    datestart=data.get('datestart'), datelimit=data.get('datelimit'),
                    usr=request.user_id, company=request.company_id).createTask()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una tarea', 'id': res})

@app_task.route(path='/gettask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettask(request):
    res = await Task(id=request.path_params.get('id')).getTask()
    pqrs = []
    if res:
        for r in res:
            closed = ""
            if r.closed:
                closed = r.closed.strftime('%Y/%m/%d')
            pqrs.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'obs': r.obs,
                'created': r.created.strftime('%Y/%m/%d'),
                'datestart': r.datestart.strftime('%Y/%m/%d'),
                'datelimit': r.datelimit.strftime('%Y/%m/%d'),
                'pqrs': r.pqrs_id,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una tarea', 'result': pqrs})

@app_task.route(path='/changedatestart', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DateTaskODM)
async def changedatestart(request):
    data: dict = await request.json()
    res = await Task(id=data.get('id'), date=data.get('date'),
                    usr=request.user_id, company=request.company_id).ChangeDateStartTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha de inicio de una tarea'})

@app_task.route(path='/changedatelimit', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DateTaskODM)
async def changedatelimit(request):
    data: dict = await request.json()
    res = await Task(id=data.get('id'), date=data.get('date'),
                    usr=request.user_id, company=request.company_id).ChangeDateLimitTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha limite de cierre de una tarea'})

@app_task.route(path='/changeresp', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UserTaskODM)
async def changeresp(request):
    data: dict = await request.json()
    res = await Task(id=data.get('id'), user=data.get('user'),
                    usr=request.user_id, company=request.company_id).ChangeRespTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar el responsable de una tarea'})

@app_task.route(path='/pendtask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendtask(request):
    res = await Task(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).PendTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente una tarea'})

@app_task.route(path='/closetask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def closetask(request):
    res = await Task(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).CloseTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada una tarea'})

@app_task.route(path='/delivertask', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DeliverObsODM)
async def delivertask(request):
    data: dict = await request.json()
    res = await Task(id=data.get('id'), obs=data.get('obs'),
                    usr=request.user_id, company=request.company_id).DeliverTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente por apeobar una tarea'})

@app_task.route(path='/deletetask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deletetask(request):
    res = await Task(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).DeleteTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular una tarea'})

@app_task.route(path='/updateobs', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdateObsODM)
async def uodateobs(request):
    data: dict = await request.json()
    res = await Task(id=data.get('id'), obs=data.get('obs'),
                    usr=request.user_id, company=request.company_id).UpdateObsTask()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar las observaciones de una tarea'})

@app_task.route(path='/gettaskuserpend/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskuserpend(request):
    res = await Task(id=request.path_params.get('id')).getTaskUserPend()
    tasks = []
    if res:
        for r in res:
            closed = ""
            if r.closed:
                closed = r.closed.strftime('%Y/%m/%d')
            tasks.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'obs': r.obs,
                'created': r.created.strftime('%Y/%m/%d'),
                'datestart': r.datestart.strftime('%Y/%m/%d'),
                'datelimit': r.datelimit.strftime('%Y/%m/%d'),
                'pqrs': r.pqrs_id,
                'pqrs_message': r.pqrs.message,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de tareas pendientes para un usuario', 'result': tasks})

@app_task.route(path='/gettaskuser/{id}/{page}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskuser(request):
    res = await Task(id=request.path_params.get('id'),page=request.path_params.get('page')).getTaskUser()
    tasks = []
    if res:
        for r in res:
            closed = ""
            if r.closed:
                closed = r.closed.strftime('%Y/%m/%d')
            tasks.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'obs': r.obs,
                'created': r.created.strftime('%Y/%m/%d'),
                'datestart': r.datestart.strftime('%Y/%m/%d'),
                'datelimit': r.datelimit.strftime('%Y/%m/%d'),
                'pqrs': r.pqrs_id,
                'pqrs_message': r.pqrs.message,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta historico de tareas para un usuario', 'result': tasks})

@app_task.route(path='/gettaskpqrs/{pqrs}/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskuser(request):
    res = await Task(pqrs=request.path_params.get('pqrs'),user=request.path_params.get('user')).getTaskPqrs()
    tasks = []
    if res:
        for r in res:
            closed = ""
            if r.closed:
                closed = r.closed.strftime('%Y/%m/%d')
            tasks.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'obs': r.obs,
                'created': r.created.strftime('%Y/%m/%d'),
                'datestart': r.datestart.strftime('%Y/%m/%d'),
                'datelimit': r.datelimit.strftime('%Y/%m/%d'),
                'pqrs': r.pqrs_id,
                'pqrs_message': r.pqrs.message,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email,
                'close': r.close
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta listado de tareas para una pqrs', 'result': tasks})
