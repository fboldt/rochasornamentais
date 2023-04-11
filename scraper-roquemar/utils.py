import os
import json
from database import Connection
from time import sleep

CURRENT_USER = os.path.expanduser('~')


def write_json(data):
    os.remove('./result.json')
    print('Write file result JSON\n')
    with open('./result.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _move_files():
    print('Moving downloaded files\n')

    DOWNLOAD_PATH = os.listdir(CURRENT_USER + '/Downloads')

    for file_name in DOWNLOAD_PATH:
        _file = file_name.split('.')
        if 'bib' in _file[len(_file) - 1]:
            src = CURRENT_USER + '/Downloads/' + file_name
            dst = r'./download/' + file_name

            print('\nMoving', src, dst)
            os.rename(src, dst)
        else:
            continue

    print('---'*5 + '\n')


def _list_files(dirname=r'./download'):
    return os.listdir(dirname)


def get_files():
    '''
    Retornando a lista de arquivos baixados.
    '''

    _move_files()

    sleep(5)

    return _list_files()


def _not_none(value):
    return value if value is not None else ''


def _formate_article(data):
    articles = []
    article = {}
    for info in data:
        article['doi'] = _not_none(info['doi'])
        article['title'] = _not_none(info['title'])
        article['author'] = _not_none(info['author'])
        article['url'] = _not_none(info['url'])
        article['year'] = _not_none(info['year'])
        article['abstract'] = _not_none(info['abstract'])

        try:
            article['references'] = _not_none(info['references'])
        except:
            article['references'] = _not_none(info['cited-references'])

        article['journal'] = _not_none(info['journal'])
        article['impact_factor'] = 0
        article['ordinatio'] = 0
        article['number-of-cited-references'] = 0

        for value in article:
            if article[value] != '' and article[value] is not None and type(article[value]) != int:
                article[value] = article[value].replace('{', '')
                article[value] = article[value].replace('}', '')

        article['relevant'] = None

        articles.append(article)
        article = {}

    return articles


def save_articles():
    data = json.load(open('./result.json', encoding='utf8'))
    dict_data = json.dumps(data)

    formated_articles = _formate_article(json.loads(dict_data))

    print('Saving data\n')
    Connection().insert('article', formated_articles)
    Connection().close()


def update_articles(df):
    print('\nUpdate Articles')

    conn = Connection()
    for _, row in df.iterrows():
        _values = {
            'year': row.get('year'),
            'journal': row.get('journal'),
            'impact_factor': row.get('impact_factor'),
            'ordinatio': row.get('ordinatio'),
            'number-of-cited-references': row.get('number-of-cited-references')
        }
        _filter = {
            'id': row.get('_id')
        }
        conn.update_one('article', _filter, _values)
    conn.close()
