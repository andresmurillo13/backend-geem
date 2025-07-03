from datetime import datetime, timezone
from geem.utils.emails import createMail
from tortoise.expressions import Q
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelTask, ModelPqrs, ModelClaimantType, ModelAreas, ModelSpecialparameters

class Task:

    def __init__(self, id="", pqrs="", user_resp = "", description="", status="", obs="", created="", closed="", datestart="",
                 datelimit="", page="", usr="", company="", date="", user=""):

        self._id = id
        self._status = status
        self._created = created
        self._closed = closed
        self._usr = usr
        self._company = company
        self._page = page
        self._pqrs = pqrs
        self._user_resp = user_resp
        self._description = description
        self._datestart = datestart
        self._datelimit = datelimit
        self._obs = obs
        self._date = date
        self._user = user


    async def createTask(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        pqrs = await ModelPqrs.get_or_none(id=self._pqrs)
        user = await ModelUser.get_or_none(id=self._user_resp)

        res = await ModelTask.create(pqrs=pqrs, user_resp=user, status=5,
                                     description=self._description, datestart=self._datestart, datelimit=self._datelimit,
                                     obs=self._obs)
        if res:
            createMail(subject="Correo Informativo SIMAF - PQRS",
                   text="Se te acaba de asignar una tarea en la pqrs con id: " + str(res.id) + "<br/> descripción: "
                        + self._description, recipient=[user.email])
            await ModelLogUser.create(event='Se crea tarea ' + str(res.id), controller='TASK', user=usr,
                                      company=comp)
            return True
        return False

    async def getTask(self):
        res = await ModelTask.filter(id=self._id).prefetch_related('pqrs', 'user_resp')
        return res

    async def ChangeDateStartTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            date_time_obj = datetime.strptime(self._date, '%Y-%m-%d')
            exist.datestart = date_time_obj
            if exist.status == 5:
                exist.status = 1
            res = await exist.save()
            if res:
                await ModelLogUser.create(event='Se modifica fecha comienzo tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
                return True
            return False
        return False

    async def ChangeDateLimitTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            date_time_obj = datetime.strptime(self._date, '%Y-%m-%d')
            exist.datelimit = date_time_obj
            if exist.status == 5:
                exist.status = 1
            res = await exist.save()
            if res:
                await ModelLogUser.create(event='Se modifica fecha limite de tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
                return True
            return False
        return False

    async def ChangeRespTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        user = await ModelUser.get_or_none(id=self._user)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist and user:
            exist.user_resp = user
            if exist.status == 5:
                exist.status = 1
            await exist.save()
            await ModelLogUser.create(event='Se modifica usuario responsable de la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)

            createMail(subject="Correo Informativo SIMAF - PQRS",
                           text="Se te asigno como responsable para su gestión la pqrs con id: " + str(exist.id) + "<br/> descripción: "
                        + exist.description, recipient=[user.email])
            return True
        return False

    async def PendTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 1
            await exist.save()
            user = await ModelUser.get_or_none(id=exist.user_resp_id)
            createMail(subject="Correo Informativo SIMAF - PQRS",
                       text="Se dejo como pendiente la tarea : " + str(exist.id) + " de la pqrs " + str(
                           exist.pqrs_id) + "<br/> descripción: "
                            + exist.description, recipient=[user.email])
            await ModelLogUser.create(event='Se deja en estado pendiente la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
            return True
        return False

    async def CloseTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 2
            await exist.save()
            exist.closed = datetime.now()
            user = await ModelUser.get_or_none(id=exist.user_resp_id)
            createMail(subject="Correo Informativo SIMAF - PQRS",
                       text="Se cerro satisfactoriamente la tarea : " + str(exist.id) + " de la pqrs " + str(
                           exist.pqrs_id) + "<br/> descripción: "
                            + exist.description, recipient=[user.email])
            pends = await ModelTask.filter(status__in=[1, 4, 5], pqrs_id=exist.pqrs_id)
            if not pends:
                resp = await ModelSpecialparameters.get_or_none(id=1)
                user_resp = await ModelUser.get_or_none(id=resp.user_pqrs_id)
                createMail(subject="Correo Informativo SIMAF - PQRS",
                           text="La pqrs  : " + str(
                               exist.pqrs_id) + " esta lista para cierre ", recipient=[user_resp.email])
            await ModelLogUser.create(event='Se deja en estado cerrada la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
            return True
        return False

    async def DeliverTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 4
            exist.obs = self._obs
            await exist.save()
            exist.closed = datetime.now()
            pqrs = await ModelPqrs.filter(id=exist.pqrs_id).prefetch_related('user_resp')
            email = ""
            for p in pqrs:
                email = p.user_resp.email
            createMail(subject="Correo Informativo SIMAF - PQRS",
                       text="Se entrego la tarea : " + str(exist.id) + " de la pqrs " + str(exist.pqrs_id) + "<br/> descripción: "
                            + exist.description, recipient=[email])
            await ModelLogUser.create(event='Se deja en estado pendiente por aprobar la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
            return True
        return False

    async def DeleteTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 3
            exist.closed = datetime.now()
            await exist.save()
            await ModelLogUser.create(event='Se deja en estado anulada la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
            return True
        return False

    async def UpdateObsTask(self):
        exist = await ModelTask.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.obs = self._obs
            if exist.status == 5:
                exist.status = 1
            res = await exist.save()
            if res:
                await ModelLogUser.create(event='Se modifica observaciones de la tarea ' + str(exist.id), controller='TASK', user=usr,
                                      company=comp)
                return True
            return False
        return False

    async def getTaskUserPend(self):
        res = await ModelTask.filter(user_resp=self._id, status__in=[1, 5]).prefetch_related('pqrs', 'user_resp')
        return res

    async def getTaskUser(self):
        limit = 10
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            res = await ModelTask.filter(user_resp=self._id).order_by('-created').limit(limit).offset(offset).prefetch_related('pqrs', 'user_resp')
        return res

    async def getTaskPqrs(self):
        if await ModelPqrs.filter(id=self._pqrs, user_resp=self._user):
            res = await ModelTask.filter(pqrs=self._pqrs).order_by('created').prefetch_related('pqrs', 'user_resp')
            for r in res:
                if r.status == 4:
                    r.close = True
                else:
                    r.close = False
            return res
        if await ModelSpecialparameters.filter(id=1, user_pqrs_id=self._user):
            res = await ModelTask.filter(pqrs=self._pqrs).order_by('created').prefetch_related('pqrs', 'user_resp')
            for r in res:
                r.close = False
            return res
        if await ModelPqrs.filter(id=self._pqrs, user=self._user):
            res = await ModelTask.filter(pqrs=self._pqrs).order_by('created').prefetch_related('pqrs', 'user_resp')
            for r in res:
                r.close = False
            return res
        res = await ModelTask.filter(user_resp=self._user, pqrs=self._pqrs).order_by('created').prefetch_related('pqrs', 'user_resp')
        for r in res:
            if r.status == 4:
                r.close = False
            else:
                r.close = False
        return res
