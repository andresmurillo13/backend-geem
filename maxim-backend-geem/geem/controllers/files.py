from datetime import datetime
from geem.utils.upload_file import delete_file

from geem.models import ModelUser, ModelCompanies, ModelFilesFindings, ModelLogUser, ModelEvents, ModelFindings, \
                        ModelTaskevents, ModelFilespqrs, ModelPqrs, ModelTask, ModelCard, ModelTaskcard


class Files:

    def __init__(self, id="", usr="", company="", url_file="", name_file="", opt="", idfile=""):

        self._id = id
        self._usr = usr
        self._company = company
        self._url_file = url_file
        self._name_file = name_file
        self._opt = opt
        self._idfile = idfile

    async def addFile(self):
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if int(self._opt) == 1:  # Events
            exist = await ModelEvents.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              events=exist, created=datetime.now(), is_active=True)

                if res:
                    await ModelLogUser.create(event='Se sube archivo al evento ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 2: # Findings
            exist = await ModelFindings.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              findings=exist, created=datetime.now())
                if res:
                    await ModelLogUser.create(event='Se sube archivo al hallazgo ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 3: # TaskEvents
            exist = await ModelTaskevents.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              task_events=exist, created=datetime.now())
                if exist.status == 5:
                    exist.status = 1
                    await exist.save()
                if res:
                    await ModelLogUser.create(event='Se sube archivo a la tarea de Evento ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 4:  # TaskEvents
            exist = await ModelPqrs.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              pqrs=exist, created=datetime.now())
                if res:
                    await ModelLogUser.create(event='Se sube archivo a la pqrs-psnc ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 5:  # TaskEvents
            exist = await ModelTask.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              task=exist, created=datetime.now())
                if exist.status == 5:
                    exist.status = 1
                    await exist.save()
                if res:
                    await ModelLogUser.create(event='Se sube archivo a la tarea de pqrs-psnc ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 6:  # TaskEvents
            exist = await ModelCard.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              card=exist, created=datetime.now())
                if res:
                    await ModelLogUser.create(event='Se sube archivo a la tarjeta ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        if int(self._opt) == 7:  # TaskEvents
            exist = await ModelTaskcard.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.create(path_complete=self._url_file, name=self._name_file, user=usr,
                                              task_card=exist, created=datetime.now())
                if exist.status == 5:
                    exist.status = 1
                    await exist.save()
                if res:
                    await ModelLogUser.create(event='Se sube archivo a la tarea de tarjeta ' + str(exist.id) + ' con nombre ' +
                                                    self._name_file, controller='FILES', user=usr, company=comp)
                    return True
                return False
            return False
        return False

    async def getFiles(self):
        if int(self._opt) == 1:  # Events
            exist = await ModelEvents.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.filter(events=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 2:  # Findings
            exist = await ModelFindings.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.filter(findings=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 3:  # TaskEvents
            exist = await ModelTaskevents.get_or_none(id=self._id)
            if exist:
                res = await ModelFilesFindings.filter(task_events=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 4:  # TaskEvents
            exist = await ModelPqrs.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.filter(pqrs_id=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 5:  # TaskEvents
            exist = await ModelTask.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.filter(task_id=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 6:  # TaskEvents
            exist = await ModelCard.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.filter(card_id=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        if int(self._opt) == 7:  # TaskEvents
            exist = await ModelTaskcard.get_or_none(id=self._id)
            if exist:
                res = await ModelFilespqrs.filter(task_card_id=exist.id).order_by('created')
                if res:
                    return res
                return []
            return False
        return False

    async def delFile(self):
        res = await ModelFilesFindings.get_or_none(id=self._idfile)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if res:
            try:
                act = delete_file(res.path_complete)
                if act:
                    await res.delete()
                    await ModelLogUser.create(event='Se borra archivo del sistema de hallazgos ' + str(res.id) + ' con nombre ' +
                                                    res.name, controller='FILES', user=usr,
                                              company=comp)
                    return True
            except Exception as error:
                return False
        return False

    async def delFilePqrs(self):
        res = await ModelFilespqrs.get_or_none(id=self._idfile)
        usr = await ModelUser.get_or_none(id=self._usr)
        comp = await ModelCompanies.get_or_none(id=self._company)
        if res:
            try:
                act = delete_file(res.path_complete)
                if act:
                    await res.delete()
                    await ModelLogUser.create(event='Se borra archivo del sistema de pqrs y tarjetas ' + str(res.id) + ' con nombre ' +
                                                    res.name, controller='FILES', user=usr,
                                              company=comp)
                    return True
            except Exception as error:
                return False
        return False