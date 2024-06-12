from viggocore.common.subsystem import operation, manager
from viggoprecificacao.subsystem.parametrizacao.plano_viggo.resource \
    import PlanoViggo


class Create(operation.Create):

    def get_codigo(self):
        domains = self.manager.api.domains().list(name='default')
        if len(domains) == 0:
            return None

        domain_id = domains[0].id
        return self.manager.api.domain_sequences().\
            get_nextval(id=domain_id, name=PlanoViggo.CODIGO_SEQUENCE)

    def pre(self, session, **kwargs):
        nome = kwargs.get('nome', None)
        if nome is None:
            raise ValueError('Nome do plano não informado.')
        kwargs['codigo'] = self.get_codigo()
        return super().pre(session=session, **kwargs)


class AddTermoAceite(operation.Update):

    def pre(self, session, id, **kwargs):
        self.termo_aceite_id = kwargs.get('termo_aceite_id', None)
        return super().pre(session=session, id=id, **kwargs)

    def do(self, session, **kwargs):
        self.entity.add_termo_aceite(self.termo_aceite_id)
        return super().do(session=session)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.add_termo_aceite = AddTermoAceite(self)
