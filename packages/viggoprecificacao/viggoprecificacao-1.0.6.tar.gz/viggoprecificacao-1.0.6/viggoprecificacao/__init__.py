import os
import viggocore

from flask_cors import CORS

from viggocore.system import System

from viggoprecificacao.packages import packages
from viggoprecificacao.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('viggoprecificacao',
                packages,
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system)

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        viggoprecificacao_database_uri = os.getenv(
            'VIGGOPRECIFICACAO_DATABASE_URI', None)
        if viggoprecificacao_database_uri is None:
            raise Exception(
                'VIGGOPRECIFICACAO_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for MySQL
            # export VIGGOPRECIFICACAO_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/viggoprecificacao
            self.config['SQLALCHEMY_DATABASE_URI'] = (
                viggoprecificacao_database_uri)
