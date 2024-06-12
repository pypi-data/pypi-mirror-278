from sqlalchemy import orm, ForeignKeyConstraint
from viggocore.database import db
from viggocore.common.subsystem import entity
from viggocore.common.utils import random_uuid


class ContratoViggo(entity.Entity, db.Model):

    CODIGO_SEQUENCE = 'contrato_viggo_codigo_sq'

    attributes = ['plano_id', 'codigo', 'observacao', 'dia_pagamento',
                  'dias_tolerancia', 'dias_permanencia', 'data_distrato',
                  'v_aquisicao', 'v_recorrente', 'valor_total_contrato',
                  'termo_aceite_mac_maquina', 'termo_aceite_aceito_dh',
                  'termo_aceite_lat', 'termo_aceite_lon',
                  'termo_aceite_atualizado', 'qtd_terminal', 'valor_terminal',
                  'customizado']
    read_only_attributes = ['v_total_produtos']
    attributes += read_only_attributes
    attributes += entity.Entity.attributes

    # ligações diretas
    plano_id = db.Column(
        db.CHAR(32), db.ForeignKey("plano_viggo.id"), nullable=False)
    plano = orm.relationship('PlanoViggo', backref=orm.backref(
        'contrato_viggo_plano_viggo'))

    # atributos
    codigo = db.Column(db.Numeric(10), nullable=False, unique=True)
    nome = db.Column(db.String(60), nullable=False)
    observacao = db.Column(db.String(250), nullable=True)
    dia_pagamento = db.Column(db.Numeric(2), nullable=True)
    dias_tolerancia = db.Column(db.Numeric(4), nullable=True)
    dias_permanencia = db.Column(db.Numeric(4), nullable=True)
    data_distrato = db.Column(db.Date(), nullable=True)
    v_aquisicao = db.Column(db.Numeric(17, 4), nullable=True)
    v_recorrente = db.Column(db.Numeric(17, 4), nullable=True)
    valor_total_contrato = db.Column(db.Numeric(17, 4), nullable=True)
    termo_aceite_mac_maquina = db.Column(db.String(20), nullable=True)
    termo_aceite_aceito_dh = db.Column(db.DateTime(), nullable=True)
    termo_aceite_lat = db.Column(db.Numeric(14, 8), nullable=True)
    termo_aceite_lon = db.Column(db.Numeric(14, 8), nullable=True)
    termo_aceite_atualizado = db.Column(db.Date(), nullable=True)
    qtd_terminal = db.Column(db.Numeric(4), nullable=True)
    valor_terminal = db.Column(db.Numeric(17, 4), nullable=True)
    customizado = db.Column(db.Boolean(), nullable=True)

    # embeddeds
    papeis = orm.relationship(
        "ContratoPapel",
        backref=orm.backref('contrato_viggo_contrato_papel'),
        cascade='delete,delete-orphan,save-update')
    servicos = orm.relationship(
        "ContratoServico",
        backref=orm.backref('contrato_viggo_contrato_servico'),
        cascade='delete,delete-orphan,save-update')
    produtos = orm.relationship(
        "ContratoProduto",
        backref=orm.backref('contrato_viggo_contrato_produto'),
        cascade='delete,delete-orphan,save-update')
    termos_aceite = orm.relationship(
        "ContratoTermoAceite",
        backref=orm.backref('contrato_viggo_contrato_termo_aceite'),
        cascade='delete,delete-orphan,save-update')

    __table_args__ = (
        ForeignKeyConstraint(['id'], ['domain.id']),)

    def __init__(self, id, plano_id, codigo, nome, observacao=None,
                 dia_pagamento=None, dias_tolerancia=None,
                 dias_permanencia=None, data_distrato=None, v_aquisicao=None,
                 v_recorrente=None, valor_total_contrato=None,
                 termo_aceite_mac_maquina=None, termo_aceite_aceito_dh=None,
                 termo_aceite_lat=None, termo_aceite_lon=None,
                 termo_aceite_atualizado=None,
                 qtd_terminal=None, valor_terminal=None, customizado=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.plano_id = plano_id
        self.codigo = codigo
        self.nome = nome
        self.observacao = observacao
        self.dia_pagamento = dia_pagamento
        self.dias_tolerancia = dias_tolerancia
        self.dias_permanencia = dias_permanencia
        self.data_distrato = data_distrato
        self.v_aquisicao = v_aquisicao
        self.v_recorrente = v_recorrente
        self.valor_total_contrato = valor_total_contrato
        self.termo_aceite_mac_maquina = termo_aceite_mac_maquina
        self.termo_aceite_aceito_dh = termo_aceite_aceito_dh
        self.termo_aceite_lat = termo_aceite_lat
        self.termo_aceite_lon = termo_aceite_lon
        self.termo_aceite_atualizado = termo_aceite_atualizado
        self.qtd_terminal = qtd_terminal
        self.valor_terminal = valor_terminal
        self.customizado = customizado

    def add_termo_aceite(self, termo_aceite_id):
        self.termos_aceite.append(
            ContratoTermoAceite(
                id=random_uuid(),
                contrato_viggo_id=self.id,
                termo_aceite_id=termo_aceite_id))
        return self

    @property
    def v_total_produtos(self):
        return sum(list(map(lambda x: x.qtd * x.valor, self.produtos)))

    @classmethod
    def individual(cls):
        return 'contrato_viggo'

    @classmethod
    def collection(cls):
        return 'contrato_viggos'

    @classmethod
    def embedded(self):
        return ['papeis', 'servicos', 'produtos']


class ContratoPapel(entity.Entity, db.Model):

    attributes = ['contrato_viggo_id', 'role_id', 'qtd', 'valor']
    attributes += entity.Entity.attributes

    # ligações diretas
    contrato_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("contrato_viggo.id"), nullable=False)
    role_id = db.Column(
        db.CHAR(32), db.ForeignKey("role.id"), nullable=False)
    role = orm.relationship('Role', backref=orm.backref(
        'contrato_papel_role'))

    # atributos
    qtd = db.Column(db.Numeric(4), nullable=True)
    valor = db.Column(db.Numeric(17, 4), nullable=True)

    def __init__(self, id, contrato_viggo_id, role_id, qtd=None, valor=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.contrato_viggo_id = contrato_viggo_id
        self.role_id = role_id
        self.qtd = qtd
        self.valor = valor

    @classmethod
    def individual(cls):
        return 'contrato_papel'

    @classmethod
    def collection(cls):
        return 'contrato_papeis'


class ContratoServico(entity.Entity, db.Model):

    attributes = ['contrato_viggo_id', 'servico_id', 'v_aquisicao',
                  'v_recorrencia', 'v_adicional', 'dias_carencia',
                  'dias_vigencia']
    attributes += entity.Entity.attributes

    # ligações diretas
    contrato_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("contrato_viggo.id"), nullable=False)
    servico_id = db.Column(
        db.CHAR(32), db.ForeignKey("servico_viggo.id"), nullable=False)
    servico = orm.relationship('ServicoViggo', backref=orm.backref(
        'contrato_servico_servico_viggo'))

    # atributos
    v_aquisicao = db.Column(db.Numeric(17, 4), nullable=True)
    v_recorrencia = db.Column(db.Numeric(17, 4), nullable=True)
    v_adicional = db.Column(db.Numeric(17, 4), nullable=True)
    dias_carencia = db.Column(db.Numeric(4), nullable=True)
    dias_vigencia = db.Column(db.Numeric(4), nullable=True)

    def __init__(self, id, contrato_viggo_id, servico_id, v_aquisicao=None,
                 v_recorrencia=None, v_adicional=None, dias_carencia=None,
                 dias_vigencia=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.contrato_viggo_id = contrato_viggo_id
        self.servico_id = servico_id
        self.v_aquisicao = v_aquisicao
        self.v_recorrencia = v_recorrencia
        self.v_adicional = v_adicional
        self.dias_carencia = dias_carencia
        self.dias_vigencia = dias_vigencia

    @classmethod
    def individual(cls):
        return 'contrato_servico'

    @classmethod
    def collection(cls):
        return 'contrato_servicos'


class ContratoProduto(entity.Entity, db.Model):

    attributes = ['contrato_viggo_id', 'produto_id', 'valor', 'qtd',
                  'qtd_dias_p_entrega', 'tem_garantia']
    attributes += entity.Entity.attributes

    # ligações diretas
    contrato_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("contrato_viggo.id"), nullable=False)
    produto_id = db.Column(
        db.CHAR(32), db.ForeignKey("produto_viggo.id"), nullable=False)
    produto = orm.relationship('ProdutoViggo', backref=orm.backref(
        'contrato_produto_produto_viggo'))

    # atributos
    valor = db.Column(db.Numeric(17, 4), nullable=True)
    qtd = db.Column(db.Numeric(17, 4), nullable=True)
    qtd_dias_p_entrega = db.Column(db.Numeric(4), nullable=True)
    tem_garantia = db.Column(db.Boolean(), nullable=True)
    dias_d_garantia = db.Column(db.Numeric(4), nullable=True)

    def __init__(self, id, contrato_viggo_id, produto_id, valor=None, qtd=None,
                 qtd_dias_p_entrega=None, tem_garantia=None,
                 dias_d_garantia=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.contrato_viggo_id = contrato_viggo_id
        self.produto_id = produto_id
        self.valor = valor
        self.qtd = qtd
        self.qtd_dias_p_entrega = qtd_dias_p_entrega
        self.tem_garantia = tem_garantia
        self.dias_d_garantia = dias_d_garantia

    @classmethod
    def individual(cls):
        return 'contrato_produto'

    @classmethod
    def collection(cls):
        return 'contrato_produtos'


class ContratoTermoAceite(entity.Entity, db.Model):

    attributes = ['contrato_viggo_id', 'termo_aceite_id']
    attributes += entity.Entity.attributes

    # ligações diretas
    contrato_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("contrato_viggo.id"), nullable=False)
    termo_aceite_id = db.Column(
        db.CHAR(32), db.ForeignKey("termo_aceite_viggo.id"), nullable=False)
    termo_aceite = orm.relationship('TermoAceiteViggo', backref=orm.backref(
        'contrato_termo_aceite_termo_aceite'))

    def __init__(self, id, contrato_viggo_id, termo_aceite_id,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.contrato_viggo_id = contrato_viggo_id
        self.termo_aceite_id = termo_aceite_id

    @classmethod
    def individual(cls):
        return 'contrato_termo_aceite'

    @classmethod
    def collection(cls):
        return 'contrato_termo_aceites'
