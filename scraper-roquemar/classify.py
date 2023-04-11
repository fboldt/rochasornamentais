import re
import bibtexparser
import pandas as pd

from database import Connection


def _get_len_references(string):
    _result = 0
    _refs = string.split('\n')
    for _ref in _refs:
        _details = _ref.split(',')
        for _item in _details:
            try:
                int(_item)
                _result += 1
            except:
                continue
    return _result


def _factors(df, df_jcr):
    _fct = []
    for journal in df['journal']:
        if df_jcr['Full Journal Title'].str.contains(journal).sum() >= 1:
            try:
                _fct.append(
                    df_jcr.loc[df_jcr['Full Journal Title'] == journal, 'Journal Impact Factor'].iloc[0])
            except:
                _fct.append(0)
        else:
            _fct.append(0)
    return _fct


def classification():
    print('\nClassification Ordinatio\n')

    # Lendo JCR xlsx
    df_jcr = pd.read_excel('./jcr_2019.xlsx')
    df_jcr['Full Journal Title'] = df_jcr['Full Journal Title'].str.upper()

    # Buscando artigos salvos no banco
    conn = Connection()
    _articles = conn.get_all('article')
    conn.close()

    # Colocando os artigos como lista do Python
    # inves do Cursor do Pymongo
    articles = []
    for _article in _articles:
        articles.append(_article)

    # Transformando em DataFrame
    df = pd.DataFrame(articles)

    # Atualizando os valores do ano para inteiro
    df['year'] = df['year'].astype(int)

    # Calculando a quantidade de referencias do artigo
    _references = []
    for ref in df['references']:
        _references.append(_get_len_references(ref))
    df['number-of-cited-references'] = _references

    # Atualizando os valores de journal para maiusculo
    df['journal'] = df['journal'].str.upper()

    # Calculando fator de impacto do artigo
    df['impact_factor'] = _factors(df, df_jcr)

    # Obtendo o valor Ordinatio e
    # ordenando o DataFrame por ele
    df['ordinatio'] = df['impact_factor'] + df['year'] - \
        2010 + df['number-of-cited-references']
    df.sort_values('ordinatio', inplace=True, ascending=False)

    return df
