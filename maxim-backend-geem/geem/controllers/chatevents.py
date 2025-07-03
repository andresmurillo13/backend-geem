from datetime import datetime, timezone
from tortoise.expressions import Q
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelFindings, ModelTaskevents, ModelChatevents


class ChatTaskEvents:

    def __init__(self, id="", finding="", user_eventtask="", message="", status="", read="", created="", closed="", usr="",
                 company="", taskevents=""):

        self._id = id
        self._status = status
        self._created = created
        self._closed = closed
        self._usr = usr
        self._company = company
        self._finding = finding
        self._user_eventtask = user_eventtask
        self._taskevents = taskevents
        self._message = message
        self._read = read


    async def createChattaskevent(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        finding = await ModelFindings.get_or_none(id=self._finding)
        user = await ModelUser.get_or_none(id=self._user_eventtask)
        taskevents = await ModelTaskevents.get_or_none(id=self._taskevents)

        res = await ModelChatevents.create(finding=finding, user_eventtask=user, status=1, taskevents=taskevents,
                                     message=self._message)
        if taskevents.status == 5:
            taskevents.status = 1
            await taskevents.save()
        await ModelLogUser.create(event='Se crea chat de evento ' + str(res.id), controller='CHAT EVENTS', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def getChattaskevent(self):
        res = await ModelChatevents.filter(taskevents_id=self._id).order_by('created').prefetch_related('finding', 'user_eventtask', 'taskevents')
        return res

    async def readChattaskevent(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        res = await ModelChatevents.filter(taskevents=self._id).update(status=2, read=datetime.now())
        if res:
            await ModelLogUser.create(event='Se marca como leido chats de evento para tarea ' + str(self._id), controller='CHAT EVENTS', user=usr,
                                      company=comp)
            return True
        return False