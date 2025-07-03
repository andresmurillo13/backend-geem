from datetime import datetime, timezone
from tortoise.expressions import Q
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelTask, ModelPqrs, ModelChat


class Chat:

    def __init__(self, id="", pqrs="", user_chat="", task="", message="", status="", read="", created="", closed="", usr="", company=""):

        self._id = id
        self._status = status
        self._created = created
        self._closed = closed
        self._usr = usr
        self._company = company
        self._pqrs = pqrs
        self._user_chat = user_chat
        self._task = task
        self._message = message
        self._read = read


    async def createChat(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        pqrs = await ModelPqrs.get_or_none(id=self._pqrs)
        user = await ModelUser.get_or_none(id=self._user_chat)
        task = await ModelTask.get_or_none(id=self._task)

        res = await ModelChat.create(pqrs=pqrs, user_chat=user, status=1, task=task,
                                     message=self._message)
        if task.status == 5:
            task.status = 1
            await task.save()
        await ModelLogUser.create(event='Se crea chat ' + str(res.id), controller='CHAT', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def getChat(self):
        res = await ModelChat.filter(task=self._id).order_by('created').prefetch_related('pqrs', 'user_chat', 'task')
        return res

    async def readChat(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        res = await ModelChat.filter(task=self._id).update(status=2, read=datetime.now())
        if res:
            await ModelLogUser.create(event='Se marca como leido chats para tarea ' + str(self._id), controller='CHAT', user=usr,
                                      company=comp)
            return True
        return False