import pymongo
from bson.objectid import ObjectId
from decouple import config


class Connection:
    """Classe conexao MongoDB

    Necessario definicao da variavel de ambiente PYTHON_ENV: `development` ou `production`.

    Caso haja login e senha para acesso ao banco definir variaveis de ambiente para login e senha: `DB_USER` `DB_PASSWORD`."""

    def __init__(self):

        if config('PYTHON_ENV') == 'development':
            self.client = pymongo.MongoClient('localhost', port=27017)
        else:
            DB_USER = config('DB_USER')
            DB_PASSWORD = config('DB_PASSWORD')
            URI = 'mongodb://' + DB_USER + ':' + DB_PASSWORD + '@ds243963.mlab.com:43963/fbro?retryWrites=false'
            self.client = pymongo.MongoClient(URI)

        self.db = self.client['fbro']

        self.tb_query = self.db['queries']
        self.tb_query_count = self.db['queries_count']
        self.tb_article = self.db['articles']
        self.tb_user = self.db['users']

    def _get_table(self, table_name: str):
        """Retorna a Collection a partir do nome."""

        if table_name == 'query':
            return self.tb_query
        elif table_name == 'article':
            return self.tb_article
        elif table_name == 'user':
            return self.tb_user
        elif table_name == 'query_count':
            return self.tb_query_count
        else:
            raise Exception("Table not defined. <", table_name, ">")

    def _get_rejector(self, rejector: dict):
        """Retorna o filtro a ser aplicado.

        O filtro deve seguir o dicionario: 

        `rejector: { 'id': 'xxx' }`"""

        [[key, value]] = rejector.items()
        if key == 'id' or key == '_id':
            return {'_id': ObjectId(value)}

    def insert(self, table_name: str, values: dict or list(dict)):
        """Inserir novo documento.

        Os valores devem ser enviado em formato de dicionario ou lista de dicionarios."""

        table = self._get_table(table_name)
        try:
            if type(values) == list:
                return table.insert_many(values)
            return table.insert_one(values)
        except Exception as exc:
            raise exc
        return False

    def get_all(self, table_name: str):
        """Retornar todos os valores; uma lista de objetos."""

        table = self._get_table(table_name)
        return table.find()

    def get_one(self, table_name: str, value: dict):
        """Retornar apenas um valor."""

        table = self._get_table(table_name)
        try:
            return table.find_one(value)
        except Exception as exc:
            raise exc
        return False

    def update_one(self, table_name: str, rejector: dict, put: dict):
        """Atualizar um Documento.

        `rejector`: o filtro unico.
            { 'id': 'xxx' }

        `put`: valores a serem atualizados.
            { 'campo': 'valor' }"""

        table = self._get_table(table_name)
        _filter = self._get_rejector(rejector)
        try:
            table.update_one(_filter, {'$set': put})
        except Exception as exc:
            raise exc
        return False

    def remove_all(self, table_name: str):
        """Apagar todos os registros de um Documento."""

        table = self._get_table(table_name)
        try:
            return table.remove({})
        except Exception as exc:
            raise exc
        return False

    def close(self):
        self.client.close()
