export default class View {
    constructor() {
        this.header = document.getElementById('navbar-collapse');
        this.alertArticles = document.getElementById('alert-without-articles');
        this.alertQueries = document.getElementById('alert-without-queries');
        this.containerArticles = document.getElementById('container-articles');
        this.containerQueries = document.getElementById('container-queries');
        this.spinnerArticles = document.getElementById('spinner-loading-articles');
        this.textSpinnerArticles = document.getElementById('text-spinner-loading-articles');
        this.spinnerQueries = document.getElementById('spinner-loading-queries');

        this.cardsArticles = [];
    }

    closeAlerts() {
        if (window.location.pathname == '/home/') {
            this.closeAlertArticles();
        } else if (window.location.pathname == '/queries/') {
            this.closeAlertQueries();
        }
    }
    closeAlertArticles() {
        this.alertArticles.style.display = 'none';
    }
    closeAlertQueries() {
        this.alertQueries.style.display = 'none';
    }
    showAlerts() {
        if (window.location.pathname == '/home/') {
            this.showAlertArticles();
        } else if (window.location.pathname == '/queries/') {
            this.showAlertQueries();
        }
    }
    showAlertArticles() {
        this.alertArticles.style.display = 'unset';
    }
    showAlertQueries() {
        this.alertQueries.style.display = 'unset';
    }

    closeSpinners() {
        if (window.location.pathname == '/home/') {
            this.closeSpinnerArticles();
        } else if (window.location.pathname == '/queries/') {
            this.closeSpinnerQueries();
        }
    }
    closeSpinnerArticles() {
        this.spinnerArticles.style.display = 'none';
        this.textSpinnerArticles.style.display = 'none';
    }
    closeSpinnerQueries() {
        this.spinnerQueries.style.display = 'none';
    }

    createContainerArticles(query, containerArticles, index) {
        const title = document.createElement('a');
        title.innerHTML = `Resultados de: <b>${query}</b>`;
        title.classList.add('btn', 'btn-primary');
        title.setAttribute('data-bs-toggle', 'collapse');
        title.href = `#collapse-container-${index}`;
        title.style.margin = '0px 0px 7px 0px';

        const container = document.createElement('div');
        container.id = `collapse-container-${index}`;
        container.classList.add('collapse');

        container.append(...containerArticles);

        this.containerArticles.append(title, container);
    }
    createCardArticle(item) {
        const card = document.createElement('div');
        card.id = `card-${item.article._id}`;
        card.classList.add('card');

        const body = document.createElement('div');
        body.classList.add('card-body');

        const title = document.createElement('h5');
        title.classList.add('card-title');
        title.innerText = item.article.title;

        const abstract = document.createElement('p');
        abstract.classList.add('card-text');
        abstract.innerText = item.article.abstract;

        const actions = document.createElement('div');
        actions.classList.add('text-end');

        const span = document.createElement('span');
        span.innerText = 'Avalie se esse Artigo é relevante para sua pesquisa: ';

        const upVote = document.createElement('a');
        upVote.id = `up-vote-${item.article._id}`;
        upVote.classList.add('btn', 'btn-outline-primary');

        const downVote = document.createElement('a');
        downVote.id = `down-vote-${item.article._id}`;
        downVote.classList.add('btn', 'btn-outline-danger');

        const upThumb = document.createElement('i');
        upThumb.classList.add('bi', 'bi-hand-thumbs-up-fill');
        const downThumb = document.createElement('i');
        downThumb.classList.add('bi', 'bi-hand-thumbs-down-fill');

        const queryId = document.createElement('input');
        queryId.id = `query-table-id-${item.article._id}`;
        queryId.type = 'hidden';
        queryId.value = item.query_table_id;
        const score = document.createElement('input');
        score.id = `score-${item.article._id}`;
        score.type = 'hidden';
        score.value = item.score;

        this.relevantArticle({
            article: item.info,
            upVote: upVote,
            downVote: downVote
        });

        upVote.append(upThumb);
        downVote.append(downThumb);

        actions.append(span, upVote, downVote);
        body.append(title, abstract, actions, queryId, score);
        card.append(body);

        // this.containerArticles.append(card);
        return card;
    }
    relevantArticle({ article, upVote = null, downVote = null }) {
        if (article[1]) {
            upVote.classList.remove('btn-outline-primary');
            upVote.classList.add('btn-primary');
            downVote.classList.add('btn-outline-danger');
            downVote.classList.remove('btn-danger');
        } else if (article[1] === false) {
            downVote.classList.remove('btn-outline-danger');
            downVote.classList.add('btn-danger');
            upVote.classList.add('btn-outline-primary');
            upVote.classList.remove('btn-primary');
        }
    }
    setArticles(queryToArticles) {
        let index = 0;
        let container = [];
        for (let query in queryToArticles) {
            for (let article of queryToArticles[query]) {
                let card = this.createCardArticle(article);
                container.push(card);
            }
            this.createContainerArticles(query, container, index);
            index++;
            container = [];
        }
    }

    createListQueries(id, query, index) {
        const li = document.createElement('li');
        li.classList.add('list-group-item');
        li.innerText = query;
        li.id = `query-${index}-${id}`;

        // const a = document.createElement('a');
        // a.classList.add('btn', 'btn-outline-danger');

        // const trash = document.createElement('i');
        // trash.classList.add('bi', 'bi-trash');

        // a.append(trash);
        // li.append(a);

        return li;
    }
    setQueries(job) {
        const ul = document.createElement('ul');
        ul.classList.add('list-group', 'list-group-flush');

        let index = 0;
        for (let j of job.querys) {
            let li = this.createListQueries(job._id, j, index);
            index++;
            ul.append(li);
        }

        this.containerQueries.append(ul);
    }

    getQuery() {
        return document.getElementById('input-query');
    }

    onButtonClick(value = null, command) {
        return async () => {
            if (value) await command(value);
            else await command();
        };
    }
    configureButton(elem, command) {
        elem.button.addEventListener('click', this.onButtonClick(elem, command));
    }
    configureInput(command) {
        const formInputQuery = document.getElementById('insert-query');
        formInputQuery.addEventListener('submit', this.onButtonClick(null, command));
    }

    configureInputQuery() {
        const inputQuery = document.getElementById('input-query');
        const btnInputQuery = document.getElementById('btn-input-query');

        btnInputQuery.disabled = true;
        inputQuery.addEventListener('keyup', () => {
            if (inputQuery.value === "") {
                btnInputQuery.disabled = true;
            } else {
                btnInputQuery.disabled = false;
            }
        });
    }
}
