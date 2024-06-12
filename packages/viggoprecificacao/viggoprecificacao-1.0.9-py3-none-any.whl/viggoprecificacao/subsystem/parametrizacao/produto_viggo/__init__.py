from viggocore.common import subsystem
from viggoprecificacao.subsystem.parametrizacao.produto_viggo \
    import resource, manager


subsystem = subsystem.Subsystem(resource=resource.ProdutoViggo,
                                manager=manager.Manager)
