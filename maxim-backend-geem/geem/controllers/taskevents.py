from datetime import datetime, timezone
from geem.utils.emails import createMail
from tortoise.expressions import Q
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelTaskevents, ModelFindings, ModelEvents, ModelActiontask


class Taskevents:

    def __init__(self, id="", description="", usr="", company="", page="", key="", effectiv="", status="", areas="",
                 user="", finding="", action_task="", created_e="", closed_e="", description_close="", description_evidence=""):

        self._id = id
        self._usr = usr
        self._company = company
        self._page = page
        self._key = key
        self._description = description
        self._effectiv = effectiv
        self._status = status
        self._areas = areas
        self._user = user
        self._finding = finding
        self._action_task = action_task
        self._created_e = created_e
        self._closed_e = closed_e
        self._description_close = description_close
        self._description_evidence = description_evidence


    async def createTaskevent(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        created = datetime.now()
        res = await ModelTaskevents.create(description=self._description, user_id=self._user, actiontask_id=self._action_task,
                                           finding_id=self._finding, created_e=self._created_e, status=5,
                                           area_id=self._areas)
        if res.id:
            actiont = await ModelActiontask.get_or_none(id=self._action_task)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se te ha asignado como responsable de la tarea con id: " + str(res.id) + "<br/> descripcion: "
                            + self._description + "<br/> tipo tarea: " + actiont.description, recipient=[usr.email])
            await ModelLogUser.create(event='Se crea la tarea de hallazgo ' + str(res.id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def updateTaskevent(self):
        taskevent = await ModelTaskevents.get_or_none(id=self._id)
        if taskevent:
            usr = await ModelUser.get_or_none(id=self._usr)
            comp = await ModelCompanies.get_or_none(id=self._company)
            updated = datetime.now()

            taskevent.description = self._description
            taskevent.description_close = self._description_close
            taskevent.description_evidence = self._description_evidence
            taskevent.user_id = self._user
            taskevent.actiontask_id = self._action_task
            taskevent.finding_id = self._finding
            taskevent.created_e = self._created_e
            if self._closed_e != "":
                taskevent.closed_e = self._closed_e
            taskevent.area_id = self._areas
            taskevent.updated = updated
            taskevent.effectiv = self._effectiv
            taskevent.status = self._status

            await taskevent.save()

            await ModelLogUser.create(event='Se modifica la tarea de hallazgo ' + str(self._id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def getTaskevent(self):
        res = await ModelTaskevents.filter(id=self._id).prefetch_related('user', 'area', 'finding', 'actiontask')
        if res:
            user = await ModelUser.get_or_none(id=self._usr)
            for r in res:
                resp = await ModelFindings.filter(id=r.finding_id, user_id=user.id).prefetch_related('event')
                if r.status == 1 or r.status == 5:
                    if resp:
                        re = await ModelTaskevents.filter(id=self._id, user=user.id)
                        if re:
                            r.createblock = True
                            r.deliverblock = True
                            r.closeblock = False
                            r.update = True
                            r.close = False
                            r.activate = False
                            r.delete = True
                            r.delivery = True
                        else:
                            r.createblock = True
                            r.deliverblock = False
                            r.closeblock = False
                            r.update = True
                            r.close = False
                            r.activate = False
                            r.delete = True
                            r.delivery = False
                    else:
                        r.createblock = False
                        r.deliverblock = True
                        r.closeblock = False
                        r.update = False
                        r.close = False
                        r.activate = False
                        r.delete = False
                        r.delivery = True
                if r.status == 2:
                    if resp:
                        r.createblock = False
                        r.deliverblock = False
                        r.closeblock = False
                        r.update = False
                        r.close = False
                        r.activate = True
                        r.delete = False
                        r.delivery = False
                    else:
                        r.createblock = False
                        r.deliverblock = False
                        r.closeblock = False
                        r.update = False
                        r.close = False
                        r.activate = False
                        r.delete = False
                        r.delivery = False
                if r.status ==3:
                    r.createblock = False
                    r.deliverblock = False
                    r.closeblock = False
                    r.update = False
                    r.close = False
                    r.activate = False
                    r.delete = False
                    r.delivery = False
                if r.status == 4:
                    if resp:
                        r.createblock = False
                        r.deliverblock = False
                        r.closeblock = True
                        r.update = False
                        r.close = True
                        r.activate = False
                        r.delete = False
                        r.delivery = False
                    else:
                        r.createblock = False
                        r.deliverblock = False
                        r.closeblock = False
                        r.update = False
                        r.close = False
                        r.activate = False
                        r.delete = False
                        r.delivery = False
        return res

    async def getTaskeventsRespFinding(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        cons = await ModelFindings.get_or_none(user_id=usr.id, id=self._finding)
        res = []
        responsable = 0
        if cons:
            res = await ModelTaskevents.filter(finding_id=self._finding).order_by(
                'status', 'created_e').prefetch_related('user', 'area', 'finding', 'actiontask')
            responsable = True
        else:
            cons2 = await ModelFindings.get_or_none(id=self._finding)
            if cons2:
                resp1 = await ModelEvents.get_or_none(id=cons2.event_id, user=usr.id)
                if resp1:
                    res = await ModelTaskevents.filter(finding_id=self._finding).order_by(
                        'status', 'created_e').prefetch_related('user', 'area', 'finding', 'actiontask')
                    responsable = False
                else:
                    res = await ModelTaskevents.filter(user_id=usr.id, finding_id=self._finding).order_by(
                        'status', 'created_e').prefetch_related('user', 'area', 'finding', 'actiontask')
                    responsable = True
        if res:
            for r in res:
                if r.status == 1 or r.status == 5:
                    r.update = True
                    r.close = False
                    r.activate = False
                    r.delete = True
                    r.delivery = True
                    r.resp = responsable
                if r.status == 2:
                    r.update = False
                    r.close = False
                    r.activate = True
                    r.delete = False
                    r.delivery = False
                    r.resp = responsable
                if r.status == 3:
                    r.update = False
                    r.close = False
                    r.activate = False
                    r.delete = False
                    r.delivery = False
                    r.resp = responsable
                if r.status == 4:
                    r.update = True
                    r.close = True
                    r.activate = False
                    r.delete = False
                    r.delivery = False
                    r.resp = responsable
            return res
        return res

    async def getTaskeventsResp(self):
        limit = 10
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [1, 2, 3, 5]
            usr = await ModelUser.get_or_none(id=self._usr)
            res = await ModelTaskevents.filter(user_id=usr.id, status__in=cad).order_by(
                'status', 'created_e').limit(limit).offset(offset).prefetch_related('user', 'area', 'finding__event', 'actiontask')
            re = await ModelTaskevents.filter(user_id=usr.id, status__in=cad).order_by('status', 'created_e').count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def getTaskeventsFinding(self):
        res = await ModelTaskevents.filter(finding_id=self._finding).order_by(
                'status', 'created_e').prefetch_related('user', 'area', 'finding', 'actiontask')
        if res:
            for r in res:
                if r.status == 1 or r.status == 5:
                    r.update = True
                    r.close = False
                    r.activate = False
                    r.delete = True
                    r.delivery = True
                if r.status == 2:
                    r.update = False
                    r.close = False
                    r.activate = True
                    r.delete = False
                    r.delivery = False
                if r.status ==3:
                    r.update = False
                    r.close = False
                    r.activate = False
                    r.delete = False
                    r.delivery = False
                if r.status == 4:
                    r.update = True
                    r.close = True
                    r.activate = False
                    r.delete = False
                    r.delivery = False
        return res

    async def pendTaskevent(self):
        exist = await ModelTaskevents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 1
            exist.updated = updated
            exist.closed = None

            await exist.save()
            user = await ModelUser.get_or_none(id=exist.user_id)
            actiont = await ModelActiontask.get_or_none(id=exist.actiontask_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se ha dejado como pendiente la tarea con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo tarea: " + actiont.description,
                       recipient=[user.email])
            await ModelLogUser.create(event='Se deja en estado pendiente la tarea de hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def closeTaskevent(self):
        exist = await ModelTaskevents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            closed = datetime.now()

            exist.status = 2
            exist.closed = closed
            exist.effectiv = self._effectiv

            await exist.save()
            user = await ModelUser.get_or_none(id=exist.user_id)
            actiont = await ModelActiontask.get_or_none(id=exist.actiontask_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se ha cerrado por responsable del hallazgo de manera satisfactoria la tarea con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo hallazgo: " + actiont.description,
                       recipient=[user.email])
            pends = await ModelTaskevents.filter(status__in=[1, 4, 5], finding_id=exist.finding_id)
            if not pends:
                finding = await ModelFindings.filter(id=exist.finding_id).prefetch_related('user')
                email = ""
                for f in finding:
                    email = f.user.email
                createMail(subject="Correo Informativo SIMAF - EVENTOS",
                           text="El hallazgo  : " + str(
                               exist.finding_id) + " esta listo para cierre ", recipient=[email])
            await ModelLogUser.create(event='Se se cierra la tarea de hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def deleteTaskevent(self):
        exist = await ModelTaskevents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 3
            exist.updated = updated
            exist.closed = None

            await exist.save()
            await ModelLogUser.create(event='Se anula la tarea de hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def deliverTaskevent(self):
        exist = await ModelTaskevents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 4
            exist.updated = updated
            exist.closed = None
            exist.closed_e = self._closed_e
            exist.description_evidence = self._description_evidence
            exist.description_close = self._description_close

            await exist.save()
            finding = await ModelFindings.filter(id=exist.finding_id).prefetch_related('user')
            email = ""
            for f in finding:
                email = f.user.email
            actiont = await ModelActiontask.get_or_none(id=exist.actiontask_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Tiene pendiente por cerrar bajo eficacia la tarea con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo de tarea: " + actiont.description,
                       recipient=[email])
            await ModelLogUser.create(event='Se entrega la tarea de hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False