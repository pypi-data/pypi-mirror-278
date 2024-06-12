from viggocore.common.subsystem import operation, manager
from viggoprecificacao.subsystem.parametrizacao.produto_viggo.resource \
    import ProdutoViggo


class Create(operation.Create):
    def get_codigo(self):
        domains = self.manager.api.domains().list(name='default')
        if len(domains) == 0:
            return None

        domain_id = domains[0].id
        return self.manager.api.domain_sequences().\
            get_nextval(id=domain_id, name=ProdutoViggo.CODIGO_SEQUENCE)

    def pre(self, session, **kwargs):
        kwargs['codigo'] = self.get_codigo()
        return super().pre(session=session, **kwargs)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
