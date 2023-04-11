# Engine de Busca
Um modulo desenvolvido em `Python` para a realização de busca de artigos científicos na ferramenta de busca da CAPES.

## Utilização
```
make build
```

## Configurações
Utilize o Makefile para criar e instarlar os pacotes necessários no ambiente virtual, com o seguinte comando:
    make build

Aṕos este passo, verifique a versão do seu Google Chrome e baixe o drive do Chrome correspondente no site:
    https://chromedriver.chromium.org/downloads
Para saber a versão do seu Google Chrome, execute o seguinte comando no terminal
    google-chrome --version
Assim que finalizar o download do driver, extraia para o diretório .drivers/ e aplique a permissão de execução no driver extraido com o comando:
    chmod +x drivers/chromedriver


## Como usar o scrapper
1º - Criar um arquivo com as queries desejadas. Exemplos de queries.
    lama de beneficiamento de rochas ornamentais
    incorporation of ornamental stone sludge in concrete
    aplicação da lama de beneficiamento de rochas ornamentais

2º - Criar o arquivo de perfil(profile) com as informações para acessar a plataforma de periodicos da CAPES.
    python3 profile.py

3º - Executar o script do scrapper dentro do ambiente virtual.
    python3 run.py --profile profile.json