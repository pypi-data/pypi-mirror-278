import os
import shutil
from logging import exception
from pathlib import Path
from viggocore.common.exception import BadRequest

from viggocore.common.subsystem import operation
from viggocore.subsystem.file import manager


class Create(manager.Create):

    def do(self, session, **kwargs):
        return super().do(session, **kwargs)


class Get(operation.Get):

    def do(self, session, **kwargs):
        file = super().do(session=session, **kwargs)

        folder = self.manager.get_upload_folder(file, file.domain_id)
        filename = '{}.{}'.format(self.id, 'pdf')

        existingFile = Path(f'{folder}/{filename}')

        if existingFile.is_file() is False:
            raise exception.ViggoCoreException('File not found!')
        else:
            return folder, filename


class GetEntity(operation.Get):

    def do(self, session, **kwargs):
        return super().do(session=session, **kwargs)


class Delete(operation.Delete):

    def post(self):
        folder = self.manager.get_upload_folder(self.entity,
                                                self.entity.domain_id)
        shutil.rmtree(folder)


class Update(operation.Update):

    def __call__(self, file, **kwargs):
        self.file = file
        self.domain_id = kwargs.get('domain_id', None)
        self.user_id = kwargs.pop('user_id', None)
        return super().__call__(**kwargs)

    def pre(self, session, **kwargs):
        id = kwargs.get('id', '')
        if self.file and self.manager.allowed_file(self.file.filename):
            self.entity = self.manager.get_entity(id=id)
        else:
            e = BadRequest()
            e.message = 'file not allowed'
            raise e
        self.upload_folder = self.manager.get_upload_folder(self.entity,
                                                            self.domain_id)
        return self.entity.is_stable()

    def do(self, session, **kwargs):
        self.file.save(os.path.join(self.upload_folder, self.entity.filename))
        entity = super().do(session, **kwargs)
        return entity


class Manager(manager.Manager):

    ALLOWED_EXTENSIONS = ['pdf']

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.get = Get(self)
        self.get_entity = GetEntity(self)
        self.delete = Delete(self)
        self.update = Update(self)

    def get_upload_folder(self, entity, domain_id):
        base_folder = self._get_base_folder()
        entity_name = type(entity).__name__
        folder = os.path.join(base_folder,
                              entity_name,
                              entity.tipo_str(),
                              self.OPTIONAL_FOLDER,
                              domain_id,
                              entity.id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
