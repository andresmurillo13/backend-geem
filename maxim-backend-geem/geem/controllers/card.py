from datetime import datetime, timezone
from tortoise.expressions import Q
from geem.utils.emails import createMail
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, ModelCard, ModelPqrs, \
    ModelTaskcard, ModelSpecialparameters, ModelVersionitems, ModelAplication, ModelLocations, ModelAreas


class Card:

    def __init__(self, id="", pqrstype="", claimanttype = "", areas="", user="", companies="", user_resp="", user_boss="", first_name="",
                 last_name="", type_person="", type_document="", num_document="", email="", address="", country="", city="", state="",
                 phone="", ext="", phone2="", ext2="", score="", obs_final="", status="", created="", closed="", action="", message="",
                 site="", form="", usr="", company="", page="", pqrs="", key="", psnc="", typepsnc="", event_date="", type="",
                 document="", compa="", position="", obs="", close="", user_obs="", items="", level="", card="", simaf="", locations="",
                 zone=""):

        self._id = id
        self._pqrstype = pqrstype
        self._claimanttype = claimanttype
        self._areas = areas
        self._user = user
        self._companies = companies
        self._user_resp = user_resp
        self._user_boss = user_boss
        self._first_name = first_name
        self._last_name = last_name
        self._type_person = type_person
        self._type_document = type_document
        self._num_document = num_document
        self._email = email
        self._address = address
        self._country = country
        self._city = city
        self._state = state
        self._phone = phone
        self._ext = ext
        self._phone2 = phone2
        self._ext2 = ext2
        self._score = score
        self._obs_final = obs_final
        self._status = status
        self._created = created
        self._closed = closed
        self._action = action
        self._message = message
        self._site = site
        self._form = form
        self._usr = usr
        self._company = company
        self._page = page
        self._pqrs = pqrs
        self._key = key
        self._psnc = psnc
        self._typepsnc = typepsnc
        self._event_date = event_date
        self._type = type
        self._document = document
        self._compa = compa,
        self._position = position
        self._obs = obs
        self._close = close
        self._user_obs = user_obs
        self._items = items
        self._level = level
        self._card = card
        self._simaf = simaf
        self._locations = locations
        self._zone = zone


    async def createCard(self):
        special = await ModelSpecialparameters.get_or_none(id=1)
        if special:
            userb = await ModelUser.get_or_none(id=special.user_pqrs_id)
        else:
            userb = await ModelUser.get_or_none(id=2)
        if self._usr:
            usr = await ModelUser.get_or_none(id=self._usr)
        else:
            usr = await ModelUser.get_or_none(id=userb.id)
        if self._company:
            comp = await ModelCompanies.get_or_none(id=self._company)
        else:
            comp = await ModelCompanies.get_or_none(id=1)
        userr = None
        usero = None
        if self._user_obs:
            usero = await ModelUser.get_or_none(id=self._user_obs)
        sim = None
        if self._simaf:
            sim = await ModelAplication.get_or_none(id=self._simaf)
        loca = await ModelLocations.get_or_none(id=self._locations)
        created = datetime.now()

        res = await ModelCard.create(type=self._type, created=created, document=self._document, first_name=self._first_name,
                                    last_name=self._last_name, company=self._compa, position=self._position,
                                     obs=self._obs, action=self._action, close=self._close, site=self._site,
                                     status=4, user=usr, user_obs=usero, user_resp=userr, user_boss=userb, simaf=sim,
                                     companies_id=self._companies, locations=loca, zone=self._zone)
        createMail(subject="Correo Informativo SIMAF - TARJETAS",
                   text="Se genera tarjeta pendiente de asignar con id: " + str(res.id) + "<br/> accion: "
                        + self._action + "<br/> observaciones: " + self._obs, recipient=[userb.email])

        for i in self._items:
            r = await ModelVersionitems.get_or_none(id=i)
            await res.items.add(r)
        await ModelLogUser.create(event='Se crea tarjeta ' + str(res.id), controller='TARJETAS', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def getCard(self):
        res = await ModelCard.filter(id=self._id).prefetch_related('user', 'user_obs', 'user_resp', 'areas',
                                                                   'user_boss', 'companies', 'items', 'locations')
        return res

    async def ChangeCreatedCard(self):
        exist = await ModelCard.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            date_time_obj = datetime.strptime(self._created, '%Y-%m-%d %H:%M:%S')
            exist.created = date_time_obj
            res = await exist.save()
            await ModelLogUser.create(event='Se modifica fecha de tarjeta ' + str(exist.id), controller='TARJETAS', user=usr,
                                      company=comp)
            return True
        return False

    async def ChangeRespCard(self):
        exist = await ModelCard.get_or_none(id=self._id)
        user = await ModelUser.get_or_none(id=self._user)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        area = await ModelAreas.get_or_none(id=self._areas)
        if exist and user:
            exist.user_resp = user
            exist.areas = area
            if exist.status == 4:
                exist.status = 1
            await exist.save()
            await ModelLogUser.create(event='Se modifica usuario responsable de la tarjeta ' + str(exist.id), controller='TARJETAS', user=usr,
                                      company=comp)
            createMail(subject="Correo Informativo SIMAF - TARJETAS",
                           text="Se te asigno como responsable para su gestión la tarjeta con id: " + str(
                               exist.id) + "<br/> accion: "
                                + exist.action + "<br/> observaciones: " + exist.obs, recipient=[user.email])
            return True
        return False

    async def PendCard(self):
        exist = await ModelCard.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 1
            await exist.save()
            await ModelLogUser.create(event='Se deja en estado pendiente la tarjeta ' + str(exist.id), controller='TARJETAS', user=usr,
                                      company=comp)
            return True
        return False

    async def CloseCard(self):
        exist = await ModelCard.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 2
            exist.close = self._close
            await exist.save()
            user_resp = await ModelUser.get_or_none(id=exist.user_resp_id)
            user_created = await ModelUser.get_or_none(id=exist.user_id)
            createMail(subject="Correo Informativo SIMAF - TARJETAS",
                       text="Se cierra satisfactoriamente la tarjeta : " + str(exist.id) + "<br/> accion: "
                            + exist.action + "<br/> observaciones: " + exist.obs,
                       recipient=[user_resp.email, user_created.email])
            await ModelLogUser.create(event='Se deja en estado cerrada a tarjeta ' + str(exist.id), controller='TARJETAS', user=usr,
                                      company=comp)
            return True
        return False

    async def DeleteCard(self):
        exist = await ModelCard.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 3
            exist.close = self._close
            await exist.save()
            await ModelTaskcard.filter(card_id=self._id).update(status=3)
            await ModelLogUser.create(event='Se deja en estado anulada la tarjeta ' + str(exist.id), controller='TARJETAS', user=usr,
                                      company=comp)
            return True
        return False

    async def getLevelItems(self):
        items = await ModelVersionitems.filter(level=self._level)
        res = await ModelVersionitems.filter(level=self._level, status=1).order_by('level', 'level2').prefetch_related('version')
        if res:
            return res
        return False

    async def getObsUser(self):
        special = await ModelSpecialparameters.get_or_none(id=1)
        if special.user_card_id == int(self._user):
            res = await ModelUser.filter(is_active=True).order_by('first_name', 'last_name')
            return res
        res = await ModelUser.filter(id=self._user)
        return res

    async def GetCardUser(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3, 4]
            res = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), status__in=cad, user_id=self._user).order_by('-created').limit(limit).offset(offset).prefetch_related('user', 'user_obs', 'user_resp', 'user_boss', 'locations')
            re = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), status__in=cad, user_id=self._user).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def GetCardActivities(self):
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
                cad = [1, 2, 3, 4, 5]
            special = await ModelSpecialparameters.get_or_none(id=1)
            if special.user_card_id == int(self._user):
                res = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), status__in=cad).order_by('-created', 'id').limit(limit).offset(offset).prefetch_related('user', 'user_obs',
                                                                   'user_resp', 'user_boss', 'locations')
                re = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), status__in=cad).count()
                num = math.ceil(re / limit)
                return res, num
            cards = []
            tasks = await ModelTaskcard.filter(user_resp_id=self._user, status__in=cad)
            if tasks:
                for t in tasks:
                    cards.append(t.card_id)
            resps = await ModelCard.filter(user_resp_id=self._user, status__in=cad)
            if resps:
                for r in resps:
                    cards.append(r.id)
            users = await ModelCard.filter(user_id=self._user, status__in=cad)
            if users:
                for u in users:
                    cards.append(u.id)
            res = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), id__in=cards).order_by('-created', 'id').limit(limit).offset(offset).prefetch_related('user', 'user_obs',
                                                                   'user_resp', 'user_boss', 'locations')
            re = await ModelCard.filter((Q(action__icontains=str(self._key)) | Q(id__icontains=str(self._key))), id__in=cards).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def IsController(self):
        res = await ModelSpecialparameters.get_or_none(user_card_id=self._user)
        if res:
            return True
        return False

    async def IsResp(self):
        res = await ModelCard.get_or_none(id=self._card, user_resp=self._user)
        if res:
            return True
        return False

    async def IsCreator(self):
        res = await ModelCard.get_or_none(id=self._card, user=self._user)
        if res:
            return True
        return False

    async def GetCardPend(self):
        special = await ModelSpecialparameters.get_or_none(id=1)
        if special.user_card_id == int(self._user):
            res = await ModelCard.filter(status=1).order_by('-created', 'id'
                                            ).prefetch_related('user', 'user_obs', 'user_resp', 'user_boss', 'locations')
            return res
        cards = []
        tasks = await ModelTaskcard.filter(user_resp_id=self._user, status=1)
        if tasks:
            for t in tasks:
                cards.append(t.card_id)
        resps = await ModelCard.filter(user_resp_id=self._user, status=1)
        if resps:
            for r in resps:
                cards.append(r.id)
        res = await ModelCard.filter(status=1, id__in=cards).order_by('-created', 'id'
                                        ).prefetch_related('user', 'user_obs', 'user_resp', 'user_boss', 'locations')
        return res

    async def GetCardControllerAsign(self):
        res = await ModelCard.filter(user_boss=self._user_boss, status=4, user_resp=None).order_by('-created').prefetch_related('user', 'user_obs', 'user_resp', 'user_boss', 'locations')
        return res
