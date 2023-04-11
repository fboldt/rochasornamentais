import pymongo
from ..__errors__ import __errors__

class Connection:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', port=27017)
        self.db = self.client['lbro']

        self.tb_query = self.db.lbro_query
        self.tb_article = self.db.lbro_article
        self.tb_user = self.db.lbro_user

    def insert_article(self, article):
        try:
            self.tb_article.insert(article)
        except Exception as exc:
            __errors__(str(exc))
            pass

    def get_queries(self):
        '''
        Retorna as Querys de busca predefinidas.
        '''
        list_queries = []
        for i in self.tb_query.find():
            list_queries.append(i['query'])
        return list_queries

    def delete_query(self, values):
        try:
            self.tb_query.delete_one({ 'id': int(values['id']) })
        except Exception as e:
            __errors__(str(e))
            return False
        return True

    def get_articles(self):
        return self.tb_article.find()

    def get_last_id_inserted(self, tablename):
        if tablename == 'query':
            try:
                return self.tb_query.find().limit(1).sort([('id', pymongo.DESCENDING)])[0] 
            except:
                return {'id': 0}
        elif tablename == 'article':
            try:
                return self.tb_article.find().limit(1).sort([('id', pymongo.DESCENDING)])[0] 
            except:
                return {'id': 0}

    def insert_user(self, values):
        try:
            self.tb_user.insert_one(values)
        except pymongo.errors.DuplicateKeyError as dupKey:
            __errors__(str(dupKey))
            return { 'valid': False, 'errors': 'Email já cadastrado.' }
        except Exception as exc:
            __errors__(str(exc))
            return { 'valid': False, 'errors': 'Erro não identificado.' }
        return { 'valid': True, 'errors': '' }

    def get_user(self, email, password):
        try:
            user = self.tb_user.find_one({'email': email,'password': password})
            if user != None:
                return { 'valid': True, 'errors': '' }
            else:
                return { 'valid': False, 'errors': 'Erro na autenticação, tente novamente.' }
        except Exception as exc:
            __errors__(str(exc))

    def all_users(self):
        tam = 1
        for i in self.tb_user.find():
            tam = tam + 1
        return { 'len_users': tam }

    def close_connection(self):
        self.client.close()
