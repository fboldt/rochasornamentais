document.addEventListener('DOMContentLoaded', () => {

    Vue.component('ba-queries', {
        template: `
        <div class="actions--query">
            <div class="name-query">{{ query }}</div>
            <div class="delete-query">
                <div class="item">
                    <i class="fa fa-trash" @click="deleteQuery" ripple></i>
                </div>
            </div>
        </div>`,

        props: ['query'],

        methods: {
            getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    let cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        let cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            },
            async deleteQuery() {
                let values = JSON.stringify(
                    { 'id': this.$el.attributes.id.value });
                try {
                    let res = await fetch(`/api/query/delete/`,{
                        method: 'POST',
                        mode: 'cors',
                        headers: {
                            "X-CSRFToken": this.getCookie("csrftoken"),
                            "Accept": "application/json",
                            "Content-Type": "application/json",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        body: values 
                    });
                    if (res.ok) {
                        this.$el.style.display = 'none';
                    }
                } catch (error) {
                    console.error(error);
                }
            }
        }
    });

    Vue.component('ba-article', {
        template: `
        <div class="article">
            <div class="content">
                <div class="title">{{ title }}</div>
                <a class="link" :href="link" target="_blank">{{ link }}</a>
                <div class="info">{{ authors }}, {{ year }}</div>
                <div class="toggle">
                    <span @click="toggleText()">
                        Visualizar texto <i class="fa fa-angle-down"></i>
                    </span>
                    <div class="text" :class="{ visible: showText }">
                        {{ abstract }}<br>{{ fulldoc }}
                    </div>
                </div>
            </div>
            <div class="actions">
                <div class="item" :class="{ upvote: up }">
                    <i class="fa fa-thumbs-up" @click="upVote" ripple></i>
                </div>
                <div class="item" :class="{ downvote: down }">
                    <i class="fa fa-thumbs-down" @click="downVote" ripple></i>
                </div>
            </div>
        </div>
        `,
        
        props: ['title', 'link', 'authors', 'year', 'abstract', 'fulldoc'],

        data() {
            return {
                showText: false,
                up: false,
                down: false,
            }
        },

        methods: {
            toggleText() {
                this.showText = !this.showText;
            },

            upVote() {
                this.up = !this.up;
                this.down = false;
            },
            
            downVote() {
                this.down = !this.down;
                this.up = false;
            },
        }

    });
    
    window.app = new Vue({
        el: '#app',
        data() {
            return {
                
                listQuery: [],
                listArticles: [],

                showModal: false,

                query: '',

                emailRegister: '',
                usernameRegister: '',
                passwordRegister: '',
                passwordRegisterAgain: '',

                emailLogin: '',
                passwordLogin: '',
                
                currentPage: 1,
                recordsPerPage: 10,
                btnNext: true,
                btnPrev: false,
                listingTable: [],
            
            }
        },
        
        methods: {

            showModalQueries() {
                this.showModal = !this.showModal;
                this.$refs.inputQuery.focus();
            },

            async insertQuery() {
                let result = await this.request(JSON.stringify({ "query": this.query }), 'query', 'POST');
                this.listQuery.push(result);
                this.query = '';
                this.$refs.inputQuery.focus();
            },

            async initSearch() {
                try {
                    await this.request(JSON.stringify(this.listQuery), 'search', 'POST');
                } catch (error) {
                    console.log(error);
                }
            },

            // utils
            getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    let cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        let cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            },
            async sha256(message) {
                const msgBuffer = new TextEncoder('utf-8').encode(message);                    
                const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
                return hashHex;
            },
            async request(values, tablename, method) {
                try {
                    let response = await fetch(`/api/${tablename}/`, {
                        method: method,
                        mode: 'cors',
                        headers: {
                            "X-CSRFToken": this.getCookie("csrftoken"),
                            "Accept": "application/json",
                            "Content-Type": "application/json",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        body: values 
                    });
                    if (response.ok) {
                        return await response.json();
                    }
                } catch (error) {
                    console.log(error);
                    return false;
                }
            },

            // Authentication
            logout() {
                localStorage.removeItem('email');
                localStorage.removeItem('password');
                window.location.href = '/login/';
            },
            async login() {
                try {
                    let res = await this.request(JSON.stringify({ 
                        "email": this.emailLogin, 
                        "password": await this.sha256(this.passwordLogin)
                    }), 'login', 'POST');
                    if (res.validation) {
                        localStorage.email = this.emailLogin;
                        localStorage.password = await this.sha256(this.passwordLogin);
                        window.location.href = '/';
                    } else {
                        alert(res.errors);
                    }
                } catch (error) {
                    console.log(error);
                }
            },
            async register() {
                let tam = await this.request({}, 'all_users', 'POST');
                if (this.passwordRegister == this.passwordRegisterAgain) {
                    let password = await this.sha256(this.passwordRegister);
                    try {
                        let res = await this.request(JSON.stringify({ 
                            "username": this.usernameRegister,
                            "email": this.emailRegister, 
                            "password": password,
                            "id": tam.len_users
                        }), 'register', 'POST');
                        if (res.validation) {
                            window.location.href = '/login/';
                        } else {
                            alert(res.errors);
                        }
                    } catch (error) {
                        console.log(error)
                    }
                } else {
                    alert('As senhas são diferentes.')
                }
            },

            // Pagination
            prevPage() {
                if (this.currentPage >1){
                    this.currentPage--;
                    this.changePage(this.currentPage)
                }
            },
            nextPage() {
                if (this.currentPage < this.numPages()){
                    this.currentPage++;
                    this.changePage(this.currentPage)
                }
            },
            changePage(page) {
                if (page < 1) page  = 1;
                if (page > this.numPages()) page = this.numPages();

                this.listingTable = [];

                for (let i = (page-1) * this.recordsPerPage; i < (page * this.recordsPerPage); i++) {
                    this.listingTable.push(this.listArticles[i]);
                }
                
                if (page == 1){
                    this.btnPrev = false;
                } else {
                    this.btnPrev = true;
                }

                if (page == this.numPages()){
                    this.btnNext = false;
                } else {
                    this.btnNext = true;
                }
                window.scrollTo(0,0);
            },
            numPages() {
                return Math.ceil(this.listArticles.length / this.recordsPerPage);
            }

        },
        
        mounted() {

            (async () => {
                try {
                    let queries = await (await fetch('/api/query/')).json();
                    if (queries.length > 0) {
                        this.listQuery = queries;
                    }
                } catch (error) {
                    console.log(error);
                }
                try {
                    let articles = await (await fetch('/api/article/')).json();
                    if (articles.length > 0) {
                        this.listArticles = articles;
                        this.changePage(1);
                    }
                } catch (error) {
                    console.log(error);
                }
            })();

            if (localStorage.email)
                this.emailLogin = localStorage.email;
            if (localStorage.password)
                this.passwordLogin = localStorage.password;

        }

    });

});
