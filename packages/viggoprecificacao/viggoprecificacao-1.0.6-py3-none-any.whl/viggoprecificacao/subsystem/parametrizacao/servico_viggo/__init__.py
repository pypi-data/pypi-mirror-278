from viggocore.common import subsystem
from viggoprecificacao.subsystem.parametrizacao.servico_viggo \
    import resource, manager


subsystem = subsystem.Subsystem(resource=resource.ServicoViggo,
                                manager=manager.Manager)
