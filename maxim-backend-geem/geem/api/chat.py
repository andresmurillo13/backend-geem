from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateChatODM, UseChatODM
from geem.controllers import Chat
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_chat = Starlette()


@app_chat.route(path='/createchat', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateChatODM)
async def createchat(request):
    data: dict = await request.json()
    res = await Chat(task=data.get('task'), user_chat=data.get('user_chat'), pqrs=data.get('pqrs'),
                    message=data.get('message'), status=data.get('status'),
                    usr=request.user_id, company=request.company_id).createChat()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un chat'})

@app_chat.route(path='/getchat/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getchat(request):
    res = await Chat(id=request.path_params.get('id')).getChat()
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
                'pqrs': r.pqrs_id,
                'user_chat': r.user_chat_id,
                'user_name': r.user_chat.email,
                'task': r.task_id,
                'read': read
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una chat', 'result': chats})

@app_chat.route(path='/readchat/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def readchat(request):
    res = await Chat(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).readChat()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para marcar un chat como leido'})
