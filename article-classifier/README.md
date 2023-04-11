# Classificador de artigos

## Instalação
Gerar chaves SSH.
```shell
> ssh-keygen
```
_As chaves ficam salvas na pasta `.ssh` no diretório do usuário._

A _Chave Pública_, de extensão `.pub`, deve ser adicionada ao GitLab, em [Configurações -> Chaves SSH](https://gitlab.com/profile/keys).

Clone dos repositórios.
```shell
> git clone git@gitlab.com:bibliometria-automatizada/article-classifier.git
> cd server-lbro
```

### Instalação de Dependências
```shell
> python -m venv env
> source env/bin/activate || env\Scripts\activate
> (env) pip install -r requirements.txt
```


