import flask
import json

from viggocore.common import exception, utils
from viggocore.common.subsystem import controller


class Controller(controller.Controller):

    def _get_token(self):
        token_id = flask.request.headers.get('token', None)
        return self.manager.api.tokens().get(id=token_id)

    def _get_domain_id_default(self):
        domains = self.manager.api.domains().list(name='default')
        if not domains:
            raise exception.BadRequest(
                'Não existe um domínio default cadastrado.')
        return domains[0].id

    def get(self, id, **kwargs):
        try:
            folder, filename = self.manager.get(id=id, **kwargs)
            return flask.send_from_directory(folder, filename)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def create(self):
        values_request = flask.request.values.get('entity', None)
        file = flask.request.files.get('file', None)

        try:
            token = self._get_token()
            if not token:
                raise exception.BadRequest()

            if not file:
                raise exception.BadRequest(
                    'O file não foi passado na requisição.')

            elif file.filename.split('.')[-1] != 'pdf':
                raise exception.BadRequest(
                    'O file não é um pdf.')

            data = json.loads(values_request)
            data['user_id'] = token.user_id
            data['domain_id'] = self._get_domain_id_default()

            entity = self.manager.create(file=file, **data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        except Exception as exc:
            return flask.Response(response=str(exc),
                                  status=400)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype="application/json")

    def update(self, id):
        values_request = flask.request.values.get('entity', None)
        file = flask.request.files.get('file', None)

        try:
            token = self._get_token()
            if not token:
                raise exception.BadRequest()

            if file and file.filename.split('.')[-1] != 'pdf':
                raise exception.BadRequest(
                    'O file não é um pdf.')

            data = json.loads(values_request)
            data['user_id'] = token.user_id
            data['domain_id'] = self._get_domain_id_default()
            data['id'] = id

            entity = self.manager.update(file=file, **data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        except Exception as exc:
            return flask.Response(response=str(exc),
                                  status=400)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")
