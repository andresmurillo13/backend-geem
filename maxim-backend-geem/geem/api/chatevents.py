from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateChatEventTaskODM
from geem.controllers import ChatTaskEvents
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_chattaskevents = Starlette()


@app_chattaskevents.route(path='/createchattaskevents', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateChatEventTaskODM)
async def createchattaskevents(request):
    data: dict = await request.json()
    res = await ChatTaskEvents(taskevents=data.get('taskevents'), user_eventtask=data.get('user_eventtask'), finding=data.get('finding'),
                    message=data.get('message'),
                    usr=request.user_id, company=request.company_id).createChattaskevent()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un chat de evento'})

@app_chattaskevents.route(path='/getchattaskevents/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getchattaskevents(request):
    res = await ChatTaskEvents(id=request.path_params.get('id')).getChattaskevent()
    chats = []
    if res:
        for r in res:
            read = ""
            if r.read:
                read = r.read.strftime('%Y/%m/%d')
            chats.append({
                'id': r.id,
                'message': r.message,
                'status': r.status,
                'created': r.created.strftime('%Y/%m/%d %H:%M:%S'),
                'finding': r.finding_id,
                'user_eventtask': r.user_eventtask_id,
                'user_name': r.user_eventtask.email,
                'taskevents': r.taskevents_id,
                'read': read
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de un chat de evento', 'result': chats})

@app_chattaskevents.route(path='/readchattaskevents/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def readchattaskevents(request):
    res = await ChatTaskEvents(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).readChattaskevent()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para marcar un chat de evento como leido'})
