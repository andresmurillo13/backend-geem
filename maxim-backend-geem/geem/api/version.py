from security.decorators.secure import secure
from security.utils import ReasonEnum
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from geem.decorators import login_required

from geem.api.odm import CreateVersionODM, UseVersionODM, UpdateVersionODM, CreateVersionitemsODM, DuplicateVersionitemsODM, UseVersionitemsODM

from geem.controllers import Version
from geem.decorators.validate import validate
from geem.utils.upload_file import upload_file

app_version = Starlette()


@app_version.route(path='/createversion', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateVersionODM)
async def createversion(request):
    data: dict = await request.json()
    res = await Version(description=data.get('description'),
                    usr=request.user_id, company=request.company_id).createVersion()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de una versión'})

@app_version.route(path='/getversion/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getversion(request):
    res = await Version(id=request.path_params.get('id')).getVersion()
    version = []
    if res:
        for r in res:
            version.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'company': r.company_id,
                'version': r.version
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de una version', 'result': version})

@app_version.route(path='/updateversion', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UpdateVersionODM)
async def updateversion(request):
    data: dict = await request.json()
    res = await Version(description=data.get('description'), id=data.get('id'),
                    usr=request.user_id, company=request.company_id).updateVersion()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para actualización de una versión'})

@app_version.route(path='/deleteversion/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def deleteversion(request):
    res = await Version(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).deleteVersion()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para borrado de una versión'})

@app_version.route(path='/activateversion/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def activateversion(request):
    res = await Version(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).activateVersion()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para activación de una versión'})

@app_version.route(path='/getversions', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getversions(request):
    res = await Version(company=request.company_id).getVersions()
    version = []
    if res:
        for r in res:
            version.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'company': r.company_id,
                'version': r.version,
                'delete': r.delete,
                'update': r.update,
                'activate': r.activate,
                'duplicate': r.duplicate
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de historico de versiones', 'result': version})

@app_version.route(path='/createitem', methods=['POST'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(CreateVersionitemsODM)
async def createitem(request):
    data: dict = await request.json()
    res = await Version(description=data.get('description'), version=data.get('version'), audit=data.get('audit'),
                        level=data.get('level'), level2=data.get('level2'),
                    usr=request.user_id, company=request.company_id).createVersionitem()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para creación de un item versión'})

@app_version.route(path='/deleteitem/{id}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(UseVersionitemsODM)
async def deleteitem(request):
    res = await Version(id=request.path_params.get('id'),
                    usr=request.user_id, company=request.company_id).deleteVersionitem()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para borrar de un item versión'})

@app_version.route(path='/getitems/{version}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
async def getitems(request):
    res = await Version(version=request.path_params.get('version')).getVersionitems()
    items = []
    if res:
        for r in res:
            items.append({
                'id': r.id,
                'description': r.description,
                'status': r.status,
                'company': r.company_id,
                'version': r.version_id,
                'audit': r.audit,
                'level': r.level,
                'level2': r.level2,
                'delete': r.delete
            })
    return UJSONResponse({'message': 'Acción tramitada para consulta de items de una version', 'result': items})

@app_version.route(path='/duplicate/{version}', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
@login_required()
@validate(DuplicateVersionitemsODM)
async def duplicate(request):
    res = await Version(version=request.path_params.get('version'),
                    usr=request.user_id, company=request.company_id).duplicateVersion()
    return UJSONResponse({'ok': res, 'message': 'Acción tramitada para duplicar versión'})

