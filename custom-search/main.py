import os
from .libs.engine import SearchEngine
from .libs.__errors__ import __errors__

ROOT = os.path.dirname(os.path.abspath(__file__))

def _read_query_file():
	_list = []
	_list_used = []
	try:
		with open(ROOT + '/queries.txt') as file_queries:
			_list = file_queries.readlines()
		for sentence in _list:
			_list_used.append(sentence.strip('\n'))
	except Exception as e:
		__errors__(str(e))
		return False
	return _list_used	

def _append_query_file(query_name):
	try:
		with open(ROOT + '/queries.txt', 'a+') as file_queries:
			file_queries.write(query_name + '\n')
	except Exception as e:
		__errors__(str(e))

def start(list_queries):
	""" Inicialização do sistema.\n
	Alternando busca entre os buscadores para cada palavra chave selecionada. """

	list_queries_used = _read_query_file()

	if len(list_queries) != len(list_queries_used):
		engine = SearchEngine()

		for q in list_queries:
			try:
				if q['query'] in list_queries_used:
					pass
				else:
					print('\nSearch: ', q['query'])

					# engine.scopus(q['query'])
					engine.google(q['query'])
					# engine.wos(q['query'])

					print(q, ' inserting in txt')
					_append_query_file(q['query'])
			except Exception as e:
				__errors__(str(e))
				continue
	else:
		print('All queries already inserted.')
