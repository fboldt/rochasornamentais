import os
import sys
import convert
from scrapper import init as init_scrapper
from utils import get_files, save_articles, update_articles
from classify import classification
from datetime import datetime
from time import sleep


def main(args):
    START = datetime.now()
    print('\nStart: {}\n'.format(START))

    # inicia busca
    init_scrapper()

    # busca arquivos baixados
    files = get_files()

    # escreve json com os artigos encontrados
    # retirando duplicadas
    convert.to_json(files)

    # salva os artigos no banco
    save_articles()

    # aplicando ordenatio
    dataframe = classification()
    update_articles(dataframe)

    try:
        bibs = os.listdir(r'./download')
        for f in bibs:
            os.remove(r'./download/' + f)
        os.removedirs(r'./download')
    except FileNotFoundError:
        pass

    print('\nDuration: {}'.format(datetime.now() - START))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
