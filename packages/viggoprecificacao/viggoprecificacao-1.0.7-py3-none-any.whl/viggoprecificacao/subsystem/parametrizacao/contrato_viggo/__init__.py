from viggocore.common import subsystem
from viggoprecificacao.subsystem.parametrizacao.contrato_viggo \
    import resource, controller, manager, router


subsystem = subsystem.Subsystem(resource=resource.ContratoViggo,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)
