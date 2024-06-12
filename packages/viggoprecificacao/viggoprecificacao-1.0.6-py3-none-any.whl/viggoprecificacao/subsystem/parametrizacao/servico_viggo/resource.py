from enum import Enum
from viggocore.database import db
from viggocore.common.subsystem import entity


class SERVICO_VIGGO_FREQUENCIA(Enum):
    UNICO = 'UNICO'
    DIARIO = 'DIARIO'
    SEMANAL = 'SEMANAL'
    QUINZENAL = 'QUINZENAL'
    MENSAL = 'MENSAL'
    ANUAL = 'ANUAL'


class ServicoViggo(entity.Entity, db.Model):

    CODIGO_SEQUENCE = 'servico_viggo_codigo_sq'

    attributes = ['nome', 'descricao', 'v_aquisicao', 'v_recorrencia',
                  'v_adicional', 'qtd_min_mes', 'qtd_max_mes', 'codigo',
                  'dias_carencia', 'dias_vigencia', 'frequencia']
    attributes += entity.Entity.attributes

    codigo = db.Column(db.Numeric(10), nullable=False, unique=True)
    nome = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    v_aquisicao = db.Column(db.Numeric(17, 4), nullable=True)
    v_recorrencia = db.Column(db.Numeric(17, 4), nullable=True)
    v_adicional = db.Column(db.Numeric(17, 4), nullable=True)
    qtd_min_mes = db.Column(db.Numeric(17, 4), nullable=True)
    qtd_max_mes = db.Column(db.Numeric(17, 4), nullable=True)
    dias_carencia = db.Column(db.Numeric(4), nullable=True)
    dias_vigencia = db.Column(db.Numeric(4), nullable=True)
    frequencia = db.Column(db.Enum(SERVICO_VIGGO_FREQUENCIA),
                           nullable=True)

    def __init__(self, id, nome, descricao, v_aquisicao, v_recorrencia,
                 v_adicional, qtd_min_mes, qtd_max_mes, dias_carencia,
                 dias_vigencia, frequencia, codigo,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.nome = nome
        self.descricao = descricao
        self.v_aquisicao = v_aquisicao
        self.v_recorrencia = v_recorrencia
        self.v_adicional = v_adicional
        self.qtd_min_mes = qtd_min_mes
        self.qtd_max_mes = qtd_max_mes
        self.dias_carencia = dias_carencia
        self.dias_vigencia = dias_vigencia
        self.frequencia = frequencia
        self.codigo = codigo

    @classmethod
    def individual(cls):
        return 'servico_viggo'

    @classmethod
    def collection(cls):
        return 'servico_viggos'
