from datetime import datetime, timezone
from tortoise.expressions import Q
from geem.utils.emails import createMail
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelEvents, ModelFindings, ModelTaskevents, ModelFindingtype


class Findings:

    def __init__(self, id="", description="", correction="", action_type="", finding_type="", usr="", company="", page="",
                    key="", effectiv="", status="", repeated="", locations="", areas="", user="", events=""):

        self._id = id
        self._usr = usr
        self._company = company
        self._page = page
        self._key = key
        self._description = description
        self._correction = correction
        self._action_type = action_type
        self._finding_type = finding_type
        self._repeated = repeated
        self._effectiv = effectiv
        self._status = status
        self._locations = locations
        self._areas = areas
        self._user = user
        self._events = events


    async def createFinding(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        created = datetime.now()
        res = await ModelFindings.create(description=self._description, created=created, correction=self._correction, repeated=self._repeated,
                                    user_id=self._user, actiontype_id=self._action_type, status=1, findingtype_id=self._finding_type,
                                    location_id=self._locations, area_id=self._areas, event_id=self._events)
        if res.id:
            user = await ModelUser.get_or_none(id=self._user)
            findingtype = await ModelFindingtype.get_or_none(id=self._finding_type)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se te ha asignado como responsable del hallazgo con id: " + str(res.id) + "<br/> descripcion: "
                            + self._description + "<br/> tipo hallazgo: " + findingtype.description, recipient=[user.email])
            await ModelLogUser.create(event='Se crea hallazgo ' + str(res.id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def updateFinding(self):
        finding = await ModelFindings.get_or_none(id=self._id)
        if finding:
            usr = await ModelUser.get_or_none(id=self._usr)
            comp = await ModelCompanies.get_or_none(id=self._company)
            updated = datetime.now()

            finding.description = self._description
            finding.correction = self._correction
            finding.repeated = self._repeated
            finding.user_id = self._user
            finding.actiontype_id = self._action_type
            finding.findingtype_id = self._finding_type
            finding.location_id = self._locations
            finding.area_id = self._areas
            finding.updated = updated
            finding.effectiv = self._effectiv
            finding.status = self._status

            await finding.save()

            await ModelLogUser.create(event='Se modifica el hallazgo ' + str(self._id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def getFinding(self):
        res = await ModelFindings.filter(id=self._id).prefetch_related('user', 'actiontype', 'findingtype', 'area', 'event', 'location')
        if res:
            user = await ModelUser.get_or_none(id=self._usr)
            for r in res:
                resp = await ModelEvents.filter(id=r.event_id, user_id=user.id)
                tasks_pend = await ModelTaskevents.filter(finding_id=self._id, status__in=[1, 4, 5])
                if r.status == 1:
                    if resp:
                        r.createblock = True
                        r.deliverblock = False
                        r.closeblock = True
                        r.update = True
                        #if await ModelTaskevents.filter(finding_id=self._id):
                        if tasks_pend :
                            r.close = False
                        else:
                            r.close = True
                        r.activate = False
                        if tasks_pend:
                            r.delete = False
                        else:
                            r.delete = True
                        r.delivery = False
                    else:
                        r.createblock = False
                        r.closeblock = False
                        r.update = False
                        r.close = False
                        r.activate = False
                        r.delete = False
                        if tasks_pend:
                            r.delivery = False
                            r.deliverblock = False
                        else:
                            if await ModelTaskevents.filter(finding_id=self._id):
                                r.delivery = True
                                r.deliverblock = True
                            else:
                                r.delivery = False
                                r.deliverblock = False
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

    async def getFindingsResp(self):
        if int(self._page) == int(10000):
            limit = 100
            page = 0
        else:
            limit = 30
            page = self._page
        res = []
        if int(page) >= 0:
            offset = int(limit) * int(page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3, 4]
            usr = await ModelUser.get_or_none(id=self._usr)
            resp = await ModelTaskevents.filter(user_id=usr.id, status__in=[1, 5]).values('finding_id')
            resf = await ModelFindings.filter(user_id=usr.id).values('id')
            list = []
            for r in resp:
                list.append(r['finding_id'])
            for f in resf:
                list.append(f['id'])
            res = await ModelFindings.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), id__in=list, status__in=cad).order_by(
                'status', 'created').limit(limit).offset(offset).prefetch_related('user', 'actiontype', 'findingtype', 'area', 'event', 'location')
            re = await ModelFindings.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), id__in=list, status__in=cad).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def getFindingsUser(self):
        if int(self._page) == int(10000):
            limit = 100
            page = 0
        else:
            limit = 30
            page = self._page
        res = []
        if int(page) >= 0:
            offset = int(limit) * int(page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3, 4]
            res = await ModelFindings.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), user_id=self._usr, status__in=cad).order_by(
                'status', 'created').limit(limit).offset(offset).prefetch_related('user', 'actiontype', 'findingtype', 'area', 'event', 'location')
            re = await ModelFindings.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), user_id=self._usr, status__in=cad).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def getFindingsEvent(self):
        res = await ModelFindings.filter(event_id=self._events).order_by(
                'status', 'created').prefetch_related('user', 'actiontype', 'findingtype', 'area', 'location')
        return res

    async def pendFinding(self):
        exist = await ModelFindings.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 1
            exist.updated = updated
            exist.closed = None

            await exist.save()
            user = await ModelUser.get_or_none(id=exist.user_id)
            findingtype = await ModelFindingtype.get_or_none(id=exist.findingtype_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se ha dejado como pendiente el hallazgo con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo hallazgo: " + findingtype.description,
                       recipient=[user.email])
            await ModelLogUser.create(event='Se deja en estado pendiente el hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def closeFinding(self):
        exist = await ModelFindings.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            closed = datetime.now()

            exist.status = 2
            exist.closed = closed
            exist.effectiv = self._effectiv

            await exist.save()
            user = await ModelUser.get_or_none(id=exist.user_id)
            findingtype = await ModelFindingtype.get_or_none(id=exist.findingtype_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se ha cerrado por responsable del evento de manera satisfactoria el hallazgo con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo hallazgo: " + findingtype.description,
                       recipient=[user.email])
            pends = await ModelFindings.filter(status__in=[1, 4], event_id=exist.event_id)
            if not pends:
                event = await ModelEvents.filter(id=exist.event_id).prefetch_related('user')
                email = ""
                for e in event:
                    email = e.user.email
                createMail(subject="Correo Informativo SIMAF - EVENTOS",
                           text="El evento  : " + str(
                               exist.event_id) + " esta listo para cierre ", recipient=[email])
            await ModelLogUser.create(event='Se se cierra el hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def deleteFinding(self):
        exist = await ModelFindings.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 3
            exist.updated = updated
            exist.closed = None

            await exist.save()
            await ModelLogUser.create(event='Se anula el hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def deliverFinding(self):
        exist = await ModelFindings.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 4
            exist.updated = updated
            exist.closed = None
            exist.correction = self._correction

            await exist.save()
            event = await ModelEvents.filter(id=exist.event_id).prefetch_related('user')
            email = ""
            for e in event:
                email = e.user.email
            findingtype = await ModelFindingtype.get_or_none(id=exist.findingtype_id)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Tiene pendiente por cerrar bajo eficacia el hallazgo con id: " + str(
                           exist.id) + "<br/> descripcion: "
                            + exist.description + "<br/> tipo hallazgo: " + findingtype.description,
                       recipient=[email])
            await ModelLogUser.create(event='Se entrega el hallazgo ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False
