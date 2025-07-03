from datetime import datetime, timezone
from tortoise.expressions import Q
from geem.utils.emails import createMail
import math

from geem.models import ModelUser, ModelCompanies, ModelLogUser, Modelpqrstype, ModelPqrs, ModelTask, ModelAreas, \
    ModelSpecialparameters, ModelAplication, ModelLocations


class Psnc:

    def __init__(self, id="", pqrstype="", claimanttype = "", areas="", user="", companies="", user_resp="", user_boss="", first_name="",
                 last_name="", type_person="", type_document="", num_document="", email="", address="", country="", city="", state="",
                 phone="", ext="", phone2="", ext2="", score="", obs_final="", status="", created="", closed="", action="", message="",
                 site="", form="", usr="", company="", page="", pqrs="", key="", psnc="", typepsnc="", event_date="", simaf="", locations=""):

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
        self._simaf = simaf
        self._locations = locations


    async def createPsnc(self):
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
        pqrst = None
        clait = None
        areas = await ModelAreas.get_or_none(id=self._areas)
        userr = None
        created = datetime.now()
        edate = self._event_date
        if edate == None:
            edate = datetime.now()
        sim = None
        if self._simaf:
            sim = await ModelAplication.get_or_none(id=self._simaf)
        loca = await ModelLocations.get_or_none(id=self._locations)
        res = await ModelPqrs.create(pqrstype=pqrst, claimanttype=clait, areas=areas, event_date=edate,
                                               user=usr, companies_id=self._companies, user_resp=userr,
                                               user_boss=userb, status=4, created=created,
                                               action=self._action, message=self._message, simaf=sim,
                                               site=self._site, form=1, psnc=2, typepsnc=self._typepsnc, locations=loca)
        createMail(subject="Correo Informativo SIMAF - PSNC",
                   text="Se genera psnc pendiente de asignar con id: " + str(res.id) + "<br/> accion: "
                        + self._action + "<br/> mensaje: " + self._message, recipient=[userb.email])
        await ModelLogUser.create(event='Se crea psnc ' + str(res.id), controller='PSNC', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def createPsncExt(self):
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
        pqrst = None
        clait = None
        areas = await ModelAreas.get_or_none(id=self._areas)
        userr = None
        created = datetime.now()
        edate = self._event_date
        sim = None
        if edate == None:
            edate = datetime.now()
        loca = await ModelLocations.get_or_none(id=self._locations)

        res = await ModelPqrs.create(pqrstype=pqrst, claimanttype=clait, areas=areas, event_date=edate,
                                               user=usr, companies=comp, user_resp=userr,
                                               user_boss=userb, first_name=self._first_name, last_name=self._last_name,
                                               type_person=self._type_person, type_document=self._type_document, email=self._email,
                                               address=self._address, country=self._country, city=self._city,
                                               state=self._state, phone=self._phone, ext=self._ext,
                                               phone2=self._phone2, ext2=self._ext2, status=4, created=created,
                                               action=self._action, message=self._message, simaf=sim,
                                               site=self._site, num_document=self._num_document, form=self._form, psnc=2,
                                               typepsnc=self._typepsnc, locations=loca)
        createMail(subject="Correo Informativo SIMAF - PSNC",
                   text="Se genera psnc pendiente de asignar con id: " + str(res.id) + "<br/> accion: "
                        + self._action + "<br/> mensaje: " + self._message, recipient=[userb.email])
        await ModelLogUser.create(event='Se crea psnc ' + str(res.id), controller='PSNC', user=usr,
                                      company=comp)

        if res:
            return True
        return False

    async def getPsnc(self):
        res = await ModelPqrs.filter(id=self._id).prefetch_related('areas', 'user', 'companies',
                                                                   'user_resp', 'user_boss', 'locations')
        return res

    async def ChangeCreatedPsnc(self):
        exist = await ModelPqrs.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            date_time_obj = datetime.strptime(self._created, '%Y-%m-%d %H:%M:%S')
            exist.created = date_time_obj
            await exist.save()
            await ModelLogUser.create(event='Se modifica fecha psnc ' + str(exist.id), controller='PSNC', user=usr,
                                      company=comp)
            return True
        return False

    async def ChangeRespPsnc(self):
        exist = await ModelPqrs.get_or_none(id=self._id)
        user = await ModelUser.get_or_none(id=self._user)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist and user:
            exist.user_resp = user
            if exist.status == 4:
                exist.status = 1
            await exist.save()
            await ModelLogUser.create(event='Se modifica usuario responsable psnc ' + str(exist.id), controller='PSNC', user=usr,
                                      company=comp)
            createMail(subject="Correo Informativo SIMAF - PSNC",
                           text="Se te asigno como responsable para su gestión la psnc con id: " + str(
                               exist.id) + "<br/> accion: "
                                + exist.action + "<br/> mensaje: " + exist.message, recipient=[user.email])
            return True
        return False

    async def PendPsnc(self):
        exist = await ModelPqrs.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 1
            await exist.save()
            await ModelLogUser.create(event='Se deja en estado pendiente el psnc ' + str(exist.id), controller='PSNC', user=usr,
                                      company=comp)
            return True
        return False

    async def ClosePsnc(self):
        exist = await ModelPqrs.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 2
            exist.obs_final = self._obs_final
            await exist.save()
            user_resp = await ModelUser.get_or_none(id=exist.user_resp_id)
            user_created = await ModelUser.get_or_none(id=exist.user_id)
            createMail(subject="Correo Informativo SIMAF - PSNC",
                       text="Se cierra satisfactoriamente la psnc : " + str(exist.id) + "<br/> accion: "
                            + exist.action + "<br/> mensaje: " + exist.message,
                       recipient=[user_resp.email, user_created.email])
            await ModelLogUser.create(event='Se deja en estado cerrado el psnc ' + str(exist.id), controller='PSNC', user=usr,
                                      company=comp)
            return True
        return False

    async def DeletePsnc(self):
        exist = await ModelPqrs.get_or_none(id=self._id)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if exist:
            exist.status = 3
            exist.obs_final = self._obs_final
            await exist.save()
            await ModelTask.filter(pqrs_id=self._id).update(status=3)
            await ModelLogUser.create(event='Se deja en estado anulado el psnc ' + str(exist.id), controller='PSNC', user=usr,
                                      company=comp)
            return True
        return False

    async def GetPsncUser(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3, 4]
            cad2 = [self._typepsnc]
            if self._typepsnc == 0:
                cad2 = [1, 2]
            res = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), user=self._user, status__in=cad, typepsnc__in=cad2, psnc=2).order_by('-created').limit(limit).offset(offset).prefetch_related('areas', 'user', 'companies',
                                                                   'user_resp', 'user_boss', 'locations')
            re = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), user=self._user, status__in=cad, typepsnc__in=cad2, psnc=2).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def GetPsncActivities(self):
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
            cad_form = [self._form]
            if self._form == 0:
                cad_form = [1, 2]
            cad_type = [self._typepsnc]
            if self._typepsnc == 0:
                cad_type = [1, 2]
            special = await ModelSpecialparameters.get_or_none(id=1)
            if special.user_pqrs_id == int(self._user):
                res = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, psnc=2, form__in=cad_form, typepsnc__in=cad_type).order_by('-created', 'id').limit(limit).offset(offset).prefetch_related('areas', 'user', 'companies',
                                         'user_resp', 'user_boss', 'locations')
                re = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, psnc=2, form__in=cad_form, typepsnc__in=cad_type).count()
                num = math.ceil(re / limit)
                return res, num
            pqrs = []
            tasks = await ModelTask.filter(user_resp_id=self._user, status__in=[1, 5])
            if tasks:
                for t in tasks:
                    pqrs.append(t.pqrs_id)
            resps = await ModelPqrs.filter(user_resp_id=self._user, status__in=cad, psnc=2, form__in=cad_form, typepsnc__in=cad_type)
            if resps:
                for r in resps:
                    pqrs.append(r.id)
            users = await ModelPqrs.filter(user_id=self._user, status__in=cad, psnc=2, form__in=cad_form, typepsnc__in=cad_type)
            if users:
                for u in users:
                    pqrs.append(u.id)
            res = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, id__in=pqrs, psnc=2, form__in=cad_form, typepsnc__in=cad_type).order_by('-created', 'id').limit(limit).offset(offset).prefetch_related('areas', 'user', 'companies',
                                         'user_resp', 'user_boss', 'locations')
            re = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, id__in=pqrs, psnc=2, form__in=cad_form, typepsnc__in=cad_type).count()
            num = math.ceil(re / limit)
            return res, num
        return res, 0

    async def GetPsncController(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3, 4]
            cad2 = [self._typepsnc]
            if self._typepsnc == 0:
                cad2 = [1, 2]
            res = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), status__in=cad, typepsnc__in=cad2, psnc=2).order_by('-created').limit(limit).offset(offset).prefetch_related('areas', 'user', 'companies',
                                                                   'user_resp', 'user_boss', 'locations')
        return res

    async def GetPsncResp(self):
        limit = 30
        res = []
        if int(self._page) >= 0:
            offset = int(limit) * int(self._page)
            cad = [self._status]
            if self._status == 0:
                cad = [1, 2, 3]
            cad2 = [self._typepsnc]
            if self._typepsnc == 0:
                cad2 = [1, 2]
            res = await ModelPqrs.filter((Q(message__icontains=str(self._key)) | Q(id__icontains=self._key)), user_resp=self._user_resp, status__in=cad,
                                         typepsnc__in=cad2, psnc=2).order_by('-created').limit(limit).offset(
                offset).prefetch_related('areas', 'user', 'companies',
                                         'user_resp', 'user_boss', 'locations')
        return res

    async def IsController(self):
        res = await ModelSpecialparameters.get_or_none(user_pqrs_id=self._user)
        if res:
            return True
        return False

    async def IsResp(self):
        res = await ModelPqrs.get_or_none(id=self._psnc, user_resp=self._user)
        if res:
            return True
        return False

    async def IsCreator(self):
        res = await ModelPqrs.get_or_none(id=self._psnc, user=self._user)
        if res:
            return True
        return False

    async def GetPsncRespPend(self):
        res = await ModelPqrs.filter(user_resp=self._user_resp, status=1, psnc=2).order_by('-created').prefetch_related('areas', 'user', 'companies','user_resp', 'user_boss', 'locations')
        return res

    async def GetPsncControllerPend(self):
        res = await ModelPqrs.filter(user_boss=self._user_boss, status=1, psnc=2).order_by('-created').prefetch_related('areas', 'user', 'companies','user_resp', 'user_boss', 'locations')
        return res

    async def GetPsncControllerAsign(self):
        res = await ModelPqrs.filter(user_boss=self._user_boss, status=4, user_resp=None, psnc=2).order_by('-created').prefetch_related('areas', 'user', 'companies','user_resp', 'user_boss', 'locations')
        return res
