import Util from './util.mjs';

export default class Auth {
    constructor({ connection }) {
        this.connection = connection;
        this.user = {};
    }

    register() {
        const formRegister = document.getElementById('register-user');

        formRegister.addEventListener('submit', async () => {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const hash = await Util.sha256(password);

            try {
                const user = await this.connection.registerUser({
                    name: name,
                    email: email,
                    password: hash,
                });

                await this.connection.createJob({ user: user.email });

                location.reload();
            } catch (error) {
                console.error(error);
            }
        });
    }

    login() {
        const formLogin = document.getElementById('login-user');

        formLogin.addEventListener('submit', async () => {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const hash = await Util.sha256(password);

            try {
                this.user = await this.connection.getUser({
                    email: email,
                    password: hash,
                });

                if (this.user == null) {
                    this.loginInvalid();
                    return;
                }

                localStorage.setItem('user', JSON.stringify(this.user));

                window.location = '/';
            } catch (error) {
                console.error(error);
            }
        });
    }

    logout() {
        const logout = document.getElementById('logout');

        logout.addEventListener('submit', () => {
            localStorage.removeItem('user');
            window.location = '/auth/entrar/';
        });
    }

    loginInvalid() {
        const alert = document.getElementById('login-invalid');
        alert.style.display = 'unset';
    }
}
