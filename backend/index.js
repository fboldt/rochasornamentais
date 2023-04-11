const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');

const { connection } = require('./util/common');
const api = require('./api');

const app = express();
const PORT = process.env.PORT || 8000;

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use('/api', api);

mongoose.connect(connection, { useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false, useCreateIndex: true }, (err) => {

    if (err) throw err;
    console.log('Connected MongoDB');

    app.listen(PORT, () =>
        console.log(`Listen PORT ${PORT}`));

});
