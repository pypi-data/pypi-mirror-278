from viggocore.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {
                'action': 'Adiciona o Termo de Aceite ao PlanoViggo',
                'method': 'PUT',
                'url': self.resource_url + '/add_termo_aceite',
                'callback': 'add_termo_aceite'
            }
        ]
