from sqlalchemy import orm
from viggocore.database import db
from viggocore.common.subsystem import entity
from viggocore.common.utils import random_uuid


class PlanoViggo(entity.Entity, db.Model):

    CODIGO_SEQUENCE = 'plano_viggo_codigo_sq'

    attributes = ['application_id', 'codigo', 'nome', 'descricao',
                  'v_aquisicao',
                  'v_recorrencia', 'dias_tolerancia', 'dias_permanencia',
                  'customizado', 'observacao', 'qtd_terminal',
                  'valor_terminal']
    attributes += entity.Entity.attributes

    # ligações diretas
    application_id = db.Column(
        db.CHAR(32), db.ForeignKey("application.id"), nullable=False)
    application = orm.relationship('Application', backref=orm.backref(
        'plano_viggo_application'))

    # atributos
    codigo = db.Column(db.Numeric(10), nullable=False, unique=True)
    nome = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(250), nullable=True)
    v_aquisicao = db.Column(db.Numeric(17, 4), nullable=True)
    v_recorrencia = db.Column(db.Numeric(17, 4), nullable=True)
    dias_tolerancia = db.Column(db.Numeric(4), nullable=True)
    dias_permanencia = db.Column(db.Numeric(4), nullable=True)
    customizado = db.Column(db.Boolean(), nullable=True)
    observacao = db.Column(db.String(1000), nullable=True)
    qtd_terminal = db.Column(db.Numeric(4), nullable=True)
    valor_terminal = db.Column(db.Numeric(17, 4), nullable=True)

    # embeddeds
    papeis = orm.relationship(
        "PlanoPapel",
        backref=orm.backref('plano_viggo_plano_papel'),
        cascade='delete,delete-orphan,save-update')
    servicos = orm.relationship(
        "PlanoServico",
        backref=orm.backref('plano_viggo_plano_servico'),
        cascade='delete,delete-orphan,save-update')
    produtos = orm.relationship(
        "PlanoProduto",
        backref=orm.backref('plano_viggo_plano_produto'),
        cascade='delete,delete-orphan,save-update')
    termos_aceite = orm.relationship(
        "PlanoTermoAceite",
        backref=orm.backref('plano_viggo_plano_termo_aceite'),
        cascade='delete,delete-orphan,save-update')

    def __init__(self, id, application_id, codigo, nome, descricao=None,
                 v_aquisicao=None,
                 v_recorrencia=None, dias_tolerancia=None,
                 dias_permanencia=None,
                 customizado=None, observacao=None, qtd_terminal=None,
                 valor_terminal=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.application_id = application_id
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.v_aquisicao = v_aquisicao
        self.v_recorrencia = v_recorrencia
        self.dias_tolerancia = dias_tolerancia
        self.dias_permanencia = dias_permanencia
        self.customizado = customizado
        self.observacao = observacao
        self.qtd_terminal = qtd_terminal
        self.valor_terminal = valor_terminal

    def add_termo_aceite(self, termo_aceite_id):
        self.termos_aceite.append(
            PlanoTermoAceite(
                id=random_uuid(),
                plano_viggo_id=self.id,
                termo_aceite_id=termo_aceite_id))
        return self

    @classmethod
    def individual(cls):
        return 'plano_viggo'

    @classmethod
    def collection(cls):
        return 'plano_viggos'

    @classmethod
    def embedded(self):
        return ['papeis', 'servicos', 'produtos']


class PlanoPapel(entity.Entity, db.Model):

    attributes = ['plano_viggo_id', 'role_id', 'qtd', 'valor']
    attributes += entity.Entity.attributes

    # ligações diretas
    plano_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("plano_viggo.id"), nullable=False)
    role_id = db.Column(
        db.CHAR(32), db.ForeignKey("role.id"), nullable=False)
    role = orm.relationship('Role', backref=orm.backref(
        'plano_papel_role'))

    # atributos
    qtd = db.Column(db.Numeric(4), nullable=True)
    valor = db.Column(db.Numeric(17, 4), nullable=True)

    def __init__(self, id, plano_viggo_id, role_id, qtd=None, valor=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.plano_viggo_id = plano_viggo_id
        self.role_id = role_id
        self.qtd = qtd
        self.valor = valor

    @classmethod
    def individual(cls):
        return 'plano_papel'

    @classmethod
    def collection(cls):
        return 'plano_papeis'


class PlanoServico(entity.Entity, db.Model):

    attributes = ['plano_viggo_id', 'servico_id', 'v_aquisicao',
                  'v_recorrencia', 'v_adicional', 'dias_carencia',
                  'dias_vigencia']
    read_only_attributes = ['v_total_produtos']
    attributes += read_only_attributes
    attributes += entity.Entity.attributes

    # ligações diretas
    plano_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("plano_viggo.id"), nullable=False)
    servico_id = db.Column(
        db.CHAR(32), db.ForeignKey("servico_viggo.id"), nullable=False)
    servico = orm.relationship('ServicoViggo', backref=orm.backref(
        'plano_servico_servico_viggo'))

    # atributos
    v_aquisicao = db.Column(db.Numeric(17, 4), nullable=True)
    v_recorrencia = db.Column(db.Numeric(17, 4), nullable=True)
    v_adicional = db.Column(db.Numeric(17, 4), nullable=True)
    dias_carencia = db.Column(db.Numeric(4), nullable=True)
    dias_vigencia = db.Column(db.Numeric(4), nullable=True)

    def __init__(self, id, plano_viggo_id, servico_id, v_aquisicao=None,
                 v_recorrencia=None, v_adicional=None, dias_carencia=None,
                 dias_vigencia=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.plano_viggo_id = plano_viggo_id
        self.servico_id = servico_id
        self.v_aquisicao = v_aquisicao
        self.v_recorrencia = v_recorrencia
        self.v_adicional = v_adicional
        self.dias_carencia = dias_carencia
        self.dias_vigencia = dias_vigencia

    @property
    def v_total_produto(self):
        return sum(list(map(lambda x: x.qtd * x.valor, self.produtos)))

    @classmethod
    def individual(cls):
        return 'plano_servico'

    @classmethod
    def collection(cls):
        return 'plano_servicos'


class PlanoProduto(entity.Entity, db.Model):

    attributes = ['plano_viggo_id', 'produto_id', 'valor', 'qtd',
                  'qtd_dias_p_entrega', 'tem_garantia']
    attributes += entity.Entity.attributes

    # ligações diretas
    plano_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("plano_viggo.id"), nullable=False)
    produto_id = db.Column(
        db.CHAR(32), db.ForeignKey("produto_viggo.id"), nullable=False)
    produto = orm.relationship('ProdutoViggo', backref=orm.backref(
        'plano_produto_produto_viggo'))

    # atributos
    valor = db.Column(db.Numeric(17, 4), nullable=True)
    qtd = db.Column(db.Numeric(17, 4), nullable=True)
    qtd_dias_p_entrega = db.Column(db.Numeric(4), nullable=True)
    tem_garantia = db.Column(db.Boolean(), nullable=True)

    def __init__(self, id, plano_viggo_id, produto_id, valor=None, qtd=None,
                 qtd_dias_p_entrega=None, tem_garantia=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.plano_viggo_id = plano_viggo_id
        self.produto_id = produto_id
        self.valor = valor
        self.qtd = qtd
        self.qtd_dias_p_entrega = qtd_dias_p_entrega
        self.tem_garantia = tem_garantia

    @classmethod
    def individual(cls):
        return 'plano_produto'

    @classmethod
    def collection(cls):
        return 'plano_produtos'


class PlanoTermoAceite(entity.Entity, db.Model):

    attributes = ['plano_viggo_id', 'termo_aceite_id']
    attributes += entity.Entity.attributes

    # ligações diretas
    plano_viggo_id = db.Column(
        db.CHAR(32), db.ForeignKey("plano_viggo.id"), nullable=False)
    termo_aceite_id = db.Column(
        db.CHAR(32), db.ForeignKey("termo_aceite_viggo.id"), nullable=False)
    termo_aceite = orm.relationship('TermoAceiteViggo', backref=orm.backref(
        'plano_termo_aceite_termo_aceite'))

    def __init__(self, id, plano_viggo_id, termo_aceite_id,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.plano_viggo_id = plano_viggo_id
        self.termo_aceite_id = termo_aceite_id

    @classmethod
    def individual(cls):
        return 'plano_termo_aceite'

    @classmethod
    def collection(cls):
        return 'plano_termo_aceites'
