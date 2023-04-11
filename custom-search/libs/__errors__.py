from datetime import datetime

def __errors__(log):
    ''' Metodo de escrita dos eventuais erros em um arquivo de log.\n
    Argumento:\n
        str - log do erro `string`. '''

    with open('./errors.log', 'a', encoding='utf-8') as error:
        try:
            error.write('[' + str(datetime.now()) + '] - ' + log + '\n')
            error.close()
        except UnicodeEncodeError as err:
            pass
        except Exception as err:
            pass
