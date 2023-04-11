# Servidor do Buscador
## Instalação
Gerar chaves SSH.
```shell
> ssh-keygen
```
_As chaves ficam salvas na pasta `.ssh` no diretório do usuário._

A _Chave Pública_, de extensão `.pub`, deve ser adicionada ao GitLab, em [Configurações -> Chaves SSH](https://gitlab.com/profile/keys).

Clone dos repositórios.
```shell
> git clone git@gitlab.com:bibliometria-automatizada/server-lbro.git
> cd server-lbro
> git clone git@gitlab.com:bibliometria-automatizada/custom-search.git lbro/enginesearch 
```

### Instalação de Dependências
```shell
> python -m venv env
> source env/bin/activate || env\Scripts\activate
> (env) pip install -r requirements.txt
```

### Instalação MongoDB
[Manual de instação](https://docs.mongodb.com/manual/installation/)

#### Docker
Caso prefira utilizar uma imagem Docker do MongoDB.
```shell
> docker pull mongo
> docker run -d -p 27017:27017 mongo:mongodb
> # test
> docker exec -it mongodb bash
root# mongo
> show dbs 
    test
    ...
```

## Inicialização do Servidor

Construção dos modelos no Banco de Dados
```shell
> (env) python manage.py migrate
...
> (env) python manage.py createsuperuser
    Username:
    Email (optional):
    Password: 
    Password (again):
 
> (env) python manage.py runserver
```

## Rotas de Acessos dos Usuários
#### `/`
- Página inicial.

#### `/login`
- Página de Entrada do Sistema.

#### `/register`
- Página de Cadatro de novos Usuários.

### Rota de Administração
#### `/admin`
- Página de controle do `Super User` criado.
