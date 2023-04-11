import csv
from .google import Google
from .scopus import Scopus
from .wos import WOS
from .capes import CAPES
from .database import Connection
from .__errors__ import __errors__




class SearchEngine():
    """ Classe de Busca. """

    def __init__(self):
        self.__conn = None

    def google(self, query):
        """ Método de busca no Google Scholar.\n
        Argumento:\n
            str - palavra chave para busca. """

        result = Google().search(query, 5)
        
        self.__conn = Connection()
        
        if result:
            for i in result:
                try:
                    self._insert(i)
                except Exception as exc:
                    __errors__('Error search Google Scholar ' + exc)
                    continue
        else:
            self.__conn.close_connection()
            return 

        self.__conn.close_connection()

    def scopus(self, query):
        """ Método de busca no Scopus.\n
        Argumento:\n
            str - palavra chave para busca. """

        result = Scopus().search(query)
        
        self.__conn = Connection()
        
        if result:
            for i in result:
                try:
                    self._insert(i)
                except Exception as exc:
                    __errors__('Error search Scopus ' + str(exc))
                    continue
        else:
            self.__conn.close_connection()
            return 

        self.__conn.close_connection()

    def wos(self, query):
        """ Método de busca no Web of Science.\n
        Argumento:\n
            str - palavra chave para busca. """
        for i in WOS().search(query):
            try:
                authors = i[2].split(':')
                # title, link, authors, year, abstract
                if self._write(i[0], i[1], authors[1], i[3], i[4]):
                    res = True
                else: res = False
            except Exception as exc:
                print('Error search WOS\n', exc, i)
                continue
        if res:
            print('Wrote')

    def capes(self, _profile):
        """ Método de busca no Portal CAPES.\n
        Argumento:\n
            str - palavra chave para busca. """

        capes =  CAPES()
        capes.setProfile(_profile)
        capes.configureBrowser()
        return capes
            
    def get_queries(self):
        """ Função que retorna as palavras chaves previamente definidas no arquivos `querys.txt` para busca.\n
        Retorno:\n
            list - lista das palavras chaves. """
        with open('./querys.txt', 'r') as q:
            query = q.read()
        return query.split('\n')
        # self.__conn = Connection()
        querys = []
        try:
            querys = self.__conn.get_queries()
        except Exception as exc:
            print(exc)
        return querys

    def _write_csv(self, title, link):
        """ Função para escrita do arquivo `articles.csv` com os resultados obtidos nas buscas.\n
        Argumento:\n
            str - título do artigo.
            str - link do artigo/PDF.\n
        Retorno:\n
            True - caso a inserção ocorra sem falha.
            False - caso haja algum erro. """
        with open('./articles.csv', 'a', newline='', encoding='utf-8') as f:
            print('Writing CSV')
            try:
                writer = csv.writer(f)
                if self._verify(link):
                    writer.writerow([title, link])
            except Exception as exc:
                print('Error write CSV: ', exc)
                return False
            f.close()
        return True

    def _verify(self, link):
        """ Função que verifica se artigo ja se encontra no `articles.csv`.\n
        Argumento:\n
            str - link do artigo/PDF.\n
        Retorno:\n
            True - caso ainda não tenha sido inserido.
            False - caso já exista no arquivo. """
        with open('./articles.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for _, _link in reader:
                if _link == link:
                    print('Article already inserted')
                    return False
            return True

    def _write_txt(self, title, link, authors, year, abstract):
        """ Função para escrita do arquivo `articles.txt` com os resultados obtidos nas buscas.\n
        Argumento:\n
            str - título do artigo.
            str - link do artigo/PDF.\n
        Retorno:\n
            True - caso a inserção ocorra sem falha.
            False - caso haja algum erro. """
        with open('./articles.txt', 'a', encoding='utf-8') as f:
            print('Writing')
            try:
                # if self._verify(link):
                f.write(title)
                f.write(', ')
                f.write(link)
                f.write(', ')
                f.write(authors)
                f.write(', ')
                f.write(year)
                f.write(', ')
                f.write(abstract)
                f.write('\n')
            except Exception as exc:
                print('Error write: ', exc)
                print(title)
                print(link)
                print(authors)
                print(year)
                print(abstract)
                return False
            f.close()
        return True

    def _insert(self, article):
        try:
            self.__conn.insert_article(article)
        except Exception as exc:
            print(exc, '\n')
            return False
        return True

   