from viggocore.common import subsystem
from viggoprecificacao.subsystem.parametrizacao.plano_viggo \
    import resource, controller, manager, router


subsystem = subsystem.Subsystem(resource=resource.PlanoViggo,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)
