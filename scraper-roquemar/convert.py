import bibtexparser
import json
import pandas as pd
from utils import write_json


def to_json(files):
    print('Read BibTex files\n')

    dataframes = []

    for f in files:
        _file = r'./download/' + f
        with open(_file, encoding='utf8') as output:
            bib_data = bibtexparser.load(output)
        df = pd.DataFrame(bib_data.entries)
        dataframes.append(df)

    # Unir e retirar duplicatas
    df_merge = pd.concat(dataframes)
    df_merge = df_merge.drop_duplicates(subset='ID', keep="first")

    result = df_merge.to_json(orient='records')
    parsed = json.loads(result)

    write_json(parsed)
