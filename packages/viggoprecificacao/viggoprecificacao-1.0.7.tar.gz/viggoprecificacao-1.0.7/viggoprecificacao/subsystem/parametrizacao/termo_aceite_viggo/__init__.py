from viggocore.common import subsystem
from viggoprecificacao.subsystem.parametrizacao.termo_aceite_viggo \
    import resource, controller, manager


subsystem = subsystem.Subsystem(resource=resource.TermoAceiteViggo,
                                controller=controller.Controller,
                                manager=manager.Manager)
