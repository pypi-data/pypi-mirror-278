import flask
from viggocore.common import exception, utils
from viggocore.common.subsystem import controller


class Controller(controller.Controller):

    MIMETYPE_JSON = 'application/json'

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def add_termo_aceite(self, id):
        data = flask.request.get_json()
        try:
            result = self.manager.add_termo_aceite(id=id, **data)

            response = {'plano_viggo': result.to_dict()}
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype=self.MIMETYPE_JSON)
