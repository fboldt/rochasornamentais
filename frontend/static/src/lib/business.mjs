export default class Business {
    constructor({ view, connection, auth }) {
        this.connection = connection;
        this.auth = auth;
        this.view = view;
        this.articlesIds = [];
        this.articles = [];
        this.job = [];
        let user = JSON.parse(localStorage.getItem('user'));
        this.user = {
            // id: user._id,
            id: user.email,
            email: user.email,
            name: user.name,
        };
        this.queryToArticles = {};
    }

    static initialize(deps) {
        const instance = new Business(deps);
        return instance._init();
    }

    compare(a, b) {
        if (a.info[2] > b.info[2]) {
            return 1;
        }
        if (a.info[2] < b.info[2]) {
            return -1;
        }
        return 0;
    }

    sortArticles() {
        for (let query in this.queryToArticles) {
            this.queryToArticles[query].sort(this.compare);
        }
    }

    async _init() {
        this.auth.logout();

        if (window.location.pathname == '/home/') {
            this.articlesIds = await this.connection.getArticlesIds(this.user.id);
            this.queryToArticles = await this.connection.getArticles(this.articlesIds);

            if (Object.keys(this.queryToArticles).length === 0) {
                this.view.showAlerts();
                return;
            }

            this.sortArticles();
            this.view.setArticles(this.queryToArticles);
            this.configureVotes();
            
            this.view.closeSpinners();
        } else if (window.location.pathname == '/queries/') {
            this.job = await this.connection.getQueries(this.user.id);

            if (Array.from(this.job.querys).length === 0) {
                this.view.showAlerts();
                return;
            }

            this.view.setQueries(this.job);
            // this.configureDeleteQuery();
            this.view.configureInputQuery();
            this.configureInsertQuery();
            
            this.view.closeSpinners();
        }

        console.log(this);
    }

    configureVotes() {
        for (let query in this.queryToArticles) {
            for (let articles of this.queryToArticles[query]) {
                let upVote = document.getElementById(`up-vote-${articles.article._id}`);
                let downVote = document.getElementById(`down-vote-${articles.article._id}`);
    
                this.view.configureButton({ button: upVote }, this.onClickUpVote.bind(this));
                this.view.configureButton({ button: downVote }, this.onClickDownVote.bind(this));
            }
        }
    }
    updateVote({ vote, queryId, articleId }) {
        let listArticles = this.articlesIds.find(art =>
            art._id === queryId);

        let index = 0;
        for (let article of listArticles.articles) {
            if (article[0] == articleId) {
                listArticles.articles[index] = vote;
                break;
            }
            index++;
        }

        return listArticles.articles;
    }
    async onClickUpVote(value) {
        const _id = value.button.id.split('-');

        const queryId = document.getElementById(`query-table-id-${_id[_id.length - 1]}`);
        const score = document.getElementById(`score-${_id[_id.length - 1]}`);

        const up = [
            _id[_id.length - 1],
            true,
            score.value == '' ? null : score.value,
        ];

        const articles = this.updateVote({
            vote: up,
            queryId: queryId.value,
            articleId: _id[_id.length - 1]
        });

        await this.connection.upVote({
            _id: queryId.value,
            articles: articles,
        });

        const article = await this.connection.getArticle(_id[_id.length - 1]);

        const upVote = document.getElementById(`up-vote-${article._id}`);
        const downVote = document.getElementById(`down-vote-${article._id}`);

        this.view.relevantArticle({
            article: up,
            downVote: downVote,
            upVote: upVote
        });
    }
    async onClickDownVote(value) {
        const _id = value.button.id.split('-');

        const queryId = document.getElementById(`query-table-id-${_id[_id.length - 1]}`);
        const score = document.getElementById(`score-${_id[_id.length - 1]}`);

        const down = [
            _id[_id.length - 1],
            false,
            score.value == '' ? null : score.value,
        ];

        const articles = this.updateVote({
            vote: down,
            queryId: queryId.value,
            articleId: _id[_id.length - 1]
        });

        await this.connection.downVote({
            _id: queryId.value,
            articles: articles,
        });

        const article = await this.connection.getArticle(_id[_id.length - 1]);

        const upVote = document.getElementById(`up-vote-${article._id}`);
        const downVote = document.getElementById(`down-vote-${article._id}`);

        this.view.relevantArticle({
            article: down,
            downVote: downVote,
            upVote: upVote
        });
    }

    configureDeleteQuery() {
        let index = 0;
        for (let _ of this.job.querys) {
            let query = document.getElementById(`query-${index}-${this.job._id}`);
            let button = document.querySelector(`#query-${index}-${this.job._id} a`);

            this.view.configureButton({
                query: query, button: button
            }, this.onClickDeleteQuery.bind(this));

            index++;
        }
    }
    async onClickDeleteQuery(values) {
        const id = document.getElementById(values.query.id);
        const _id = id.id.split('-');

        await this.connection.removeQuery({
            _id: _id[_id.length - 1],
            query: values.query.textContent
        });

        location.reload();
    }

    configureInsertQuery() {
        this.view.configureInput(this.onClickInsertQuery.bind(this));
    }
    async onClickInsertQuery() {
        const query = this.view.getQuery().value;

        await this.connection.insertQuery({
            id: this.job._id,
            query
        });

        location.reload();
    }
}
