if (localStorage.getItem('user')) {
    window.location = '/home/';
}

import Auth from "./lib/auth.mjs";
import Connection from "./lib/connection.mjs";

const onload = () => {
    const url = 'http://127.0.0.1:8000/api';
    const connection = new Connection({ url });
    const auth = new Auth({ connection });

    auth.login();
};

window.onload = onload;
