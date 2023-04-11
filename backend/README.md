# Backend

## Instalação

Necessário `NodeJS` versão mínima `12.18.3` e um gerenciador de dependências, como `NPM`.

### Clone repositório

```shell
> git clone git@gitlab.com:bibliometria-automatizada/backend.git
> cd backend
```

### Instalação de Dependências

```python
> npm install
```

### Variáveis de Ambiente

```python
NODE_ENV=development

# necessário definir para acessar o banco
# seja localhost ou externo
DB_USER=<usuário do banco>
DB_PASSWORD=<senha do banco>

# padrão -> localhost/fbro
HOST=<host e nome do banco>
```

---

## Necessário instalção MongoDB.

[Manual de instação](https://docs.mongodb.com/manual/installation/)

## Inicialização

```python
# Inicialização com live reload
# Equivale -> nodemon index.js
> npm run dev

# Inicialização padrão do servidor
> npm run start
```

<!--
### Modelo dos Dados
### **Query**
```javascript
query: {
    query: String,
    used: {
        type: Boolean,
        default: false,
    },
};
```

### **Article**
```javascript
article: {
    doi: String,
    title: String,
    url: String,
    author: String,
    year: Number,
    abstract: String,
    references: [],
    impact_factor: Number,
    ordinatio: Number,
    relevant: Boolean,
    'number-of-cited-references': Number,
}
```

***
## Assinaturas de Rotas

### `/`, método `GET`
**Retorno**
- `JSON`:
```javascript
{
    module: 'API FBRO',
    env: process.env.NODE_ENV
}
```

### `/insert/:tablename`, método `POST`
**Parâmetros**
- `:tablename`: O nome da tabela na qual será inserido o valor.
- `Object`: Valor a ser inserido, seguindo padrão dos Modelos de Dados.

**Retorno**
- `Object`: O valor inserido.

### `/get/all/:tablename`, método `POST`
**Parâmetros**
- `:tablename`: O nome da tabela na qual será inserido o valor.

**Retorno**
- `List[Object]`: Uma lista com todos os valores presentes na tabela, ou uma lista vázia.

### `/remove/:tablename`, método `POST`
**Parâmetro**
- `:tablename`: O nome da tabela na qual será inserido o valor.
- `Object`: Contendo ID do valor que será removido.

**Retorno**
- `Object`: Validando a exclusão ou informando o erro.

### `/update/one/:tablename`, método `POST`
**Parâmetro**
- `:tablename`: O nome da tabela na qual será inserido o valor.
- `Object`: Contendo ID do valor que será atualizado e, nesse caso, a relevância do Artigo em questão.
```javascript
{
    _id: '276349...',
    relevant: true || false,
}
```

**Retorno**
- `Object`: Valor atualizado.
 -->
