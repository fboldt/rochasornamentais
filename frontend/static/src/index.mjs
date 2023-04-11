if (!localStorage.getItem('user')) {
    window.location = '/auth/entrar/';
}

import Auth from "./lib/auth.mjs";
import Business from "./lib/business.mjs";
import Connection from "./lib/connection.mjs";
import View from "./lib/view.mjs";

const onload = () => {
    const urlServer = { url: 'http://127.0.0.1:8000/api' };

    const connection = new Connection(urlServer);
    const auth = new Auth({ connection });
    const view = new View();

    // window.testConnection = connection.testConnection();

    Business.initialize({ view, connection, auth });
};

window.onload = onload;
