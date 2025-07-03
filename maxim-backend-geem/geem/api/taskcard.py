from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateTaskcardODM, DateTaskcardODM, UpdatecardObsODM, UserTaskcardODM, DeliverCardObsODM
from geem.controllers import Taskcard
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_taskcard = Starlette()


@app_taskcard.route(path='/createtaskcard', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateTaskcardODM)
async def createtaskcard(request):
    data: dict = await request.json()
    res = await Taskcard(card=data.get('card'), user_resp=data.get('user_resp'), description=data.get('description'),
                    obs=data.get('obs'), datestart=data.get('datestart'), datelimit=data.get('datelimit'),
                    usr=request.user_id, company=request.company_id).createTaskcard()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una tarea de tarjeta'})

@app_taskcard.route(path='/gettaskcard/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskcard(request):
    res = await Taskcard(id=request.path_params.get('id')).getTaskcard()
    card = []
    if res:
        for r in res:
            closed = ""
            if r.closed:
                closed = r.closed.strftime('%Y/%m/%d')
            card.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'obs': r.obs,
                'created': r.created.strftime('%Y/%m/%d'),
                'datestart': r.datestart.strftime('%Y/%m/%d'),
                'datelimit': r.datelimit.strftime('%Y/%m/%d'),
                'card': r.card_id,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una tarea de tarjeta', 'result': card})

@app_taskcard.route(path='/changedatestart', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DateTaskcardODM)
async def changedatestart(request):
    data: dict = await request.json()
    res = await Taskcard(id=data.get('id'), date=data.get('date'),
                    usr=request.user_id, company=request.company_id).ChangeDateStartTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha de inicio de una tarea'})

@app_taskcard.route(path='/changedatelimit', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DateTaskcardODM)
async def changedatelimit(request):
    data: dict = await request.json()
    res = await Taskcard(id=data.get('id'), date=data.get('date'),
                    usr=request.user_id, company=request.company_id).ChangeDateLimitTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar la fecha limite de cierre de una tarea de tarjeta'})

@app_taskcard.route(path='/changeresp', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UserTaskcardODM)
async def changeresp(request):
    data: dict = await request.json()
    res = await Taskcard(id=data.get('id'), user=data.get('user'),
                    usr=request.user_id, company=request.company_id).ChangeRespTaskCard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar el responsable de una tarea de tarjeta.'})

@app_taskcard.route(path='/pendtask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def pendtask(request):
    res = await Taskcard(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).PendTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente una tarea de tarea'})

@app_taskcard.route(path='/closetask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def closetask(request):
    res = await Taskcard(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).CloseTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar cerrada una tarjeta de tarea'})


@app_taskcard.route(path='/delivertask', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DeliverCardObsODM)
async def delivertask(request):
    data: dict = await request.json()
    res = await Taskcard(id=data.get('id'), obs=data.get('obs'),
                    usr=request.user_id, company=request.company_id).DeliverTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para dejar pendiente por aprobación una tarjeta de tarea'})

@app_taskcard.route(path='/deletetask/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deletetask(request):
    res = await Taskcard(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).DeleteTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para anular una tarea de tarjeta'})

@app_taskcard.route(path='/updateobs', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdatecardObsODM)
async def uodateobs(request):
    data: dict = await request.json()
    res = await Taskcard(id=data.get('id'), obs=data.get('obs'),
                    usr=request.user_id, company=request.company_id).UpdateObsTaskcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para modificar las observaciones de una tarea de tarjeta'})

@app_taskcard.route(path='/gettaskcarduserpend/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskcarduserpend(request):
    res = await Taskcard(id=request.path_params.get('id')).getTaskCardUserPend()
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
                'card': r.card_id,
                'card_obs': r.card.obs,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de tareas de tarjeta pendientes para un usuario', 'result': tasks})

@app_taskcard.route(path='/gettaskcarduser/{id}/{page}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskcarduser(request):
    res = await Taskcard(id=request.path_params.get('id'),page=request.path_params.get('page')).getTaskCardUser()
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
                'card': r.card_id,
                'card_obs': r.card.obs,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta historico de tareas de tarejeta para un usuario', 'result': tasks})

@app_taskcard.route(path='/gettaskcard/{card}/{user}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def gettaskcard(request):
    res = await Taskcard(card=request.path_params.get('card'),user=request.path_params.get('user')).getTaskCard()
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
                'card': r.card_id,
                'card_obs': r.card.obs,
                'user_resp': r.user_resp_id,
                'closed': closed,
                'resp_name': r.user_resp.first_name,
                'resp_surname': r.user_resp.last_name,
                'email': r.user_resp.email,
                'close': r.close
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta listado de tareas de tarjeta para una pqrs', 'result': tasks})
