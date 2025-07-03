from datetime import datetime, timezone
from tortoise.expressions import Q
from geem.utils.emails import createMail
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelEvents, ModelFindings, ModelEventtype


class Events:

    def __init__(self, id="", description="", reporter="", date="", cost="", event_type="", usr="", company="", page="",
                    key="", effectiv="", status="", date_close="", property_damage=""):

        self._id = id
        self._usr = usr
        self._company = company
        self._page = page
        self._key = key
        self._description = description
        self._reporter = reporter
        self._date = date
        self._cost = cost
        self._event_type = event_type
        self._effectiv = effectiv
        self._status = status
        self._date_close = date_close
        self._property_damage = property_damage


    async def createEvent(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        created = datetime.now()
        res = await ModelEvents.create(description=self._description, created=created, reporter=self._reporter, date=self._date,
                                    cost=self._cost, eventtype_id=self._event_type, status=1, user=usr, property_damage=self._property_damage)
        if res.id:
            eventtype = await ModelEventtype.get_or_none(id=self._event_type)
            createMail(subject="Correo Informativo SIMAF - EVENTOS",
                       text="Se genera satisfactoriamente el evento con id: " + str(res.id) + "<br/> descripcion: "
                            + self._description + "<br/> tipo evento: " + eventtype.description, recipient=[usr.email])
            await ModelLogUser.create(event='Se crea evento ' + str(res.id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def updateEvent(self):
        event = await ModelEvents.get_or_none(id=self._id)
        if event:
            usr = await ModelUser.get_or_none(id=self._usr)
            comp = await ModelCompanies.get_or_none(id=self._company)
            updated = datetime.now()

            event.description = self._description
            event.reporter = self._reporter
            event.date = self._date
            event.cost = self._cost
            event.eventtype_id = self._event_type
            event.updated = updated
            event.user = usr
            event.effectiv = self._effectiv
            event.status = self._status
            event.property_damage = self._property_damage
            event.date_close = self._date_close

            await event.save()

            await ModelLogUser.create(event='Se modifica el evento ' + str(self._id), controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def getEvent(self):
        res = await ModelEvents.filter(id=self._id).prefetch_related('user', 'eventtype')
        if res:
            for r in res:
                finding_pend = await ModelFindings.filter(event_id=self._id, status__in=[1, 4])
                if r.status == 1:
                    r.update = True
                    if finding_pend:
                        r.close = False
                        r.delete = False
                    else:
                        if await ModelFindings.filter(event_id=self._id):
                            r.close = True
                        else:
                            r.close = False
                        r.delete = True
                    r.activate = False
                if r.status == 2:
                    r.update = False
                    r.close = False
                    r.delete = False
                    r.activate = True
                if r.status == 3:
                    r.update = False
                    r.close = False
                    r.delete = False
                    r.activate = False
        return res

    async def getEventUser(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3]
            usr = await ModelUser.get_or_none(id=self._usr)
            res = await ModelEvents.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, user_id=usr.id).order_by(
                'status', '-date').limit(limit).offset(offset).prefetch_related('user', 'eventtype')
            re = await ModelEvents.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, user_id=usr.id).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def getEvents(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3]
            res = await ModelEvents.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad).order_by(
                'status', '-date').limit(limit).offset(offset).prefetch_related('user', 'eventtype')
            re = await ModelEvents.filter((Q(description__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def pendEvent(self):
        exist = await ModelEvents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 1
            exist.updated = updated
            exist.closed = None

            await exist.save()
            await ModelLogUser.create(event='Se deja en estado pendiente el evento ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def closeEvent(self):
        exist = await ModelEvents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            closed = datetime.now()

            exist.status = 2
            exist.closed = closed
            exist.effectiv = self._effectiv
            exist.date_close = self._date_close

            await exist.save()
            await ModelLogUser.create(event='Se se cierra el evento ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False

    async def deleteEvent(self):
        exist = await ModelEvents.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            updated = datetime.now()

            exist.status = 3
            exist.updated = updated
            exist.closed = None

            await exist.save()
            await ModelLogUser.create(event='Se anula el evento ' + str(exist.id),
                                      controller='CONTROL DE HALLAZGOS', user=usr,
                                      company=comp)
            return True
        return False
