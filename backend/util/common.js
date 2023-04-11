const fs = require('fs');

const Article = require('../models/Article');
const User = require('../models/User');
const Query = require('../models/Query');
const ArticleUploaded = require('../models/ArticleUploaded');
const Job = require('../models/Job');

const multer = require('multer');
require('dotenv/config');

const dir = './upload';

if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
}

function getTable(tablename) {
    switch (tablename) {
        case 'article':
            return Article;
        case 'user':
            return User;
        case 'query':
            return Query;
        case 'articleUploaded':
            return ArticleUploaded;
        case 'job':
            return Job;
        default:
            return Error('Invalid Table Name');
    }
}

const connection = `mongodb://${process.env.DB_USER}:${process.env.DB_PASSWORD}@${process.env.HOST}`;

module.exports = {
    connection,
    getTable,
    multer: multer({
        storage: multer.diskStorage({
            destination: (req, file, cb) => {
                cb(null, dir);
            },
            filename: (req, file, cb) => {
                cb(null, Date.now().toString() + "." + file.originalname);
            }
        }),
    }),
};
