export default class Connection {
    constructor({ url }) {
        this.url = url;
    }

    async testConnection() {
        const response = await fetch(`${this.url}`, {
            method: 'GET',
            mode: 'cors',
        });
        return await response.json();
    }

    static #getOptions(body, method) {
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        };
        const optionsDefault = { method: method, mode: 'cors', headers: headers };
        const options = method === 'POST'
            ? Object.assign(optionsDefault, { body: JSON.stringify(body) }) : optionsDefault;
        return options;
    }
    async fetch({ action = '', tablename = '', params = '', body = {}, method = 'POST' }) {
        const options = Connection.#getOptions(body, method);
        try {
            const response = await fetch(`${this.url}/${action}/${tablename}/${params}`, options);
            return await response.json();
        } catch (error) {
            console.error(error);
            return error;
        }
    }

    async getArticlesIds(userId) {
        return await this.fetch({
            tablename: 'query',
            action: 'get/all',
            body: {
                userId: userId,
            },
        });
    }
    async getArticles(tableQuery) {
        let listArticleInfos = [];
        let queryToArticles = {};
        for (let query of tableQuery) {
            for (let info of query.articles) {
                let article = await this.getArticle(info[0]);
                let articleInfos = {
                    query_table_id: query._id,
                    score: info[2],
                    article,
                    info,
                };
                listArticleInfos.push(articleInfos);
            }
            queryToArticles[query.query] = listArticleInfos;
            listArticleInfos = [];
        }
        return queryToArticles;
    }
    async getArticle(id) {
        return await this.fetch({
            tablename: 'article',
            action: 'get/one',
            body: {
                _id: id,
            },
        });
    }

    async upVote(values) {
        return await this.fetch({
            tablename: 'query',
            action: 'update/relevance',
            body: values,
        });
    }
    async downVote(values) {
        return await this.fetch({
            tablename: 'query',
            action: 'update/relevance',
            body: values,
        });
    }

    async getQueries(user) {
        return await this.fetch({
            tablename: 'job',
            action: 'get/one',
            body: {
                user: user,
            },
        });
    }
    async removeQuery(values) {
        return await this.fetch({
            tablename: 'job',
            action: 'remove/query',
            body: values,
        });
    }
    async insertQuery(values) {
        return await this.fetch({
            tablename: 'job',
            action: 'insert/query',
            body: values,
        });
    }

    async registerUser(user) {
        return await this.fetch({
            tablename: 'user',
            action: 'insert',
            body: user,
        });
    }
    async getUser(user) {
        return await this.fetch({
            tablename: 'user',
            action: 'login',
            body: user,
        })
    }

    async createJob(user) {
        return await this.fetch({
            tablename: 'job',
            action: 'insert',
            body: user,
        });
    }
}
