from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateChatcardODM, UseChatcardODM
from geem.controllers import ChatCard
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_chatcard = Starlette()


@app_chatcard.route(path='/createchatcard', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateChatcardODM)
async def createchatcard(request):
    data: dict = await request.json()
    res = await ChatCard(taskcard=data.get('taskcard'), user_chatitem=data.get('user_chatitem'), card=data.get('card'),
                    message=data.get('message'), status=data.get('status'),
                    usr=request.user_id, company=request.company_id).createChatcard()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un chat de tarjeta'})

@app_chatcard.route(path='/getchatcard/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getchatcard(request):
    res = await ChatCard(id=request.path_params.get('id')).getChatcard()
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
                'card': r.card_id,
                'user_chatitem': r.user_chatitem_id,
                'user_name': r.user_chatitem.email,
                'task': r.taskcard_id,
                'read': read
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una chat de tarjeta', 'result': chats})

@app_chatcard.route(path='/readchatcard/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def readchatcard(request):
    res = await ChatCard(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).readChatcard()
    return UJSONResponse({'ok': True, 'message': 'Acción tramitada para marcar un chat de tarjeta como leido'})
