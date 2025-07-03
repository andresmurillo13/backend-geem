from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateFileODM
from geem.controllers import Files
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_files = Starlette()


@app_files.route(path='/addfile/{id}/{opt}', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateFileODM)
async def addfile(request):
    data: dict = await request.json()
    url_file = ""
    if data.get('name_file'):
        url_file = upload_file(data=data)
    res = await Files(url_file=url_file, name_file=data.get('name_file'),
                        id=request.path_params.get('id'), opt=request.path_params.get('opt'),
                        usr = request.user_id, company = request.company_id).addFile()
    return UJSONResponse({'ok': res, 'message': 'Acción para cargue de un archivo'})

@app_files.route(path='/getfiles/{id}/{opt}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getfiles(request):
    res = await Files(id=request.path_params.get('id'), opt=request.path_params.get('opt')).getFiles()
    files = []
    if res:
        for r in res:
            files.append({
                'id': r.id,
                'path_complete': r.path_complete,
                'name': r.name,
                'created': r.created.strftime('%Y/%m/%d')
            })
    return UJSONResponse({'ok': True, 'message': 'Accion para consultar archivos.', 'result': files})

@app_files.route(path='/delfile/{idfile}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def delfile(request):
    res = await Files(idfile=request.path_params.get('idfile'), usr=request.user_id, company=request.company_id).delFile()
    return UJSONResponse({'ok': res, 'message': 'Acción para borrar archivo'})

@app_files.route(path='/delfilepqrs/{idfile}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def delfilepqrs(request):
    res = await Files(idfile=request.path_params.get('idfile'), usr=request.user_id, company=request.company_id).delFilePqrs()
    return UJSONResponse({'ok': res, 'message': 'Acción para borrar archivo'})