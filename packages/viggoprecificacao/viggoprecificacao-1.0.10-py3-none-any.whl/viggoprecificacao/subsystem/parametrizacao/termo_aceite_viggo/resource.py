from enum import Enum

import sqlalchemy
from viggocore.subsystem.file.resource import File
from viggocore.database import db


class TERMO_ACEITE_VIGGO_TIPO(Enum):
    POLITICA_ACESSO = 1
    POLITICA_PRIVACIDADE = 2


class TermoAceiteViggo(File, db.Model):
    attributes = ['tipo']
    attributes += File.attributes

    id = db.Column(db.ForeignKey('file_infosys.id'), primary_key=True)
    tipo = db.Column(sqlalchemy.Enum(TERMO_ACEITE_VIGGO_TIPO),
                     nullable=False, unique=True)

    __mapper_args__ = {'polymorphic_identity': 'termo_aceite_viggo'}

    def __init__(self, id,  tipo, domain_id=None, name=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, domain_id, name, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.tipo = tipo

    def is_stable(self):
        return True

    def tipo_str(self):
        if type(self.tipo) is str:
            return self.tipo
        else:
            return self.tipo.name

    @classmethod
    def individual(cls):
        return 'termo_aceite_viggo'

    @classmethod
    def collection(cls):
        return 'termo_aceite_viggos'
