from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


from geem.api.pqrs import app_pqrs
from geem.api.task import app_task
from geem.api.chat import app_chat
from geem.api.psnc import app_psnc
from geem.api.version import app_version
from geem.api.card import app_card
from geem.api.chatcard import app_chatcard
from geem.api.taskcard import app_taskcard
from geem.api.events import app_events
from geem.api.findings import app_findings
from geem.api.taskevents import app_taskevents
from geem.api.chatevents import app_chattaskevents
from geem.api.files import app_files

app = Starlette()
app.add_middleware(CORSMiddleware, allow_methods=['POST', 'GET'], allow_origins=['*'], allow_headers=['*'])
app.add_middleware(ProxyHeadersMiddleware)

app.mount('/pqrs', app_pqrs)
app.mount('/task', app_task)
app.mount('/chat', app_chat)
app.mount('/psnc', app_psnc)
app.mount('/version', app_version)
app.mount('/card', app_card)
app.mount('/chatcard', app_chatcard)
app.mount('/taskcard', app_taskcard)
app.mount('/events', app_events)
app.mount('/findings', app_findings)
app.mount('/taskevents', app_taskevents)
app.mount('/chatevents', app_chattaskevents)
app.mount('/files', app_files)



