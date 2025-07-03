from datetime import datetime, timezone
from tortoise.expressions import Q
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelTaskcard, ModelCard, ModelChatcard


class ChatCard:

    def __init__(self, id="", card="", user_chatitem="", message="", status="", read="", created="", closed="", usr="",
                 company="", taskcard=""):

        self._id = id
        self._status = status
        self._created = created
        self._closed = closed
        self._usr = usr
        self._company = company
        self._card = card
        self._user_chatitem = user_chatitem
        self._taskcard = taskcard
        self._message = message
        self._read = read


    async def createChatcard(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        card = await ModelCard.get_or_none(id=self._card)
        user = await ModelUser.get_or_none(id=self._user_chatitem)
        taskcard = await ModelTaskcard.get_or_none(id=self._taskcard)

        res = await ModelChatcard.create(card=card, user_chatitem=user, status=1, taskcard=taskcard,
                                     message=self._message)
        if taskcard.status == 5:
            taskcard.status = 1
            await taskcard.save()
        await ModelLogUser.create(event='Se crea chat de tarjeta ' + str(res.id), controller='CHAT CARD', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def getChatcard(self):
        res = await ModelChatcard.filter(taskcard_id=self._id).order_by('created').prefetch_related('card', 'user_chatitem', 'taskcard')
        return res

    async def readChatcard(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        res = await ModelChatcard.filter(taskcard=self._id).update(status=2, read=datetime.now())
        if res:
            await ModelLogUser.create(event='Se marca como leido chats de tarjeta para tarea ' + str(self._id), controller='CHAT CARD', user=usr,
                                      company=comp)
            return True
        return False