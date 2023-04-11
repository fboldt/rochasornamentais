# Scrapper baseado no Sistema do Roquemar

## Instalação

### Clone repositório
```shell
> git clone git@gitlab.com:bibliometria-automatizada/scraper-roquemar.git scrapper
> cd scrapper
```

### Ambiente virtual
```shell
> python -m venv env
> source env/bin/activate || ./env/Scripts/activate
```

### Dependências
```shell
> (env) pip install -r requirements.txt
```

### Variáveis de ambiente
Crie um arquivo na raiz do projeto chamado `.env`.
```python
PYTHON_ENV=development

# Caso esteja rodando fora do domínio do IFES, 
# definir seu login e senha para acesso no CAFe - Periódico CAPES
LOGIN=<login IFES>
PASSWORD=<senha IFES>
```

### Necessário instalação MongoDB.
[Manual de instação](https://docs.mongodb.com/manual/installation/)


### Google Chrome
Para rodar o Scrapper é importante ter o `Google Chrome` instalado e atualizado na última versão.

Os *drivers* para o `Selenium` se encontram juntos do projeto. 

## Inicialização
```shell
> python main.py
```

Os arquivos `BibTex` são baixados no diretório de *Downloads* do usuário e posteriomente movidos para uma pasta no diretório do projeto. 

**Importante:** não manter arquivos com extensão `.bib` no diretório de *Downloads* do usuário.

<!-- ## Resultado 
É gerado um arquivo `result.json` com os artigos baixados e são salvos no Banco de Dados os mesmo com a relação de *ordinatio*. -->
