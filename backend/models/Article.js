const mongoose = require('mongoose');

const ArticleSchema = mongoose.Schema({
    doi: {
        type: String,
    },
    title: {
        type: String,
    },
    url: {
        type: String,
    },
    author: {
        type: String,
    },
    year: {
        type: Number,
    },
    abstract: {
        type: String,
    },
    references: {
        type: String,
    },
    impact_factor: {
        type: Number,
    },
    ordinatio: {
        type: Number,
    },
    'number-of-cited-references': {
        type: Number,
    },
    relevant: {
        type: Boolean,
    },
    userId: {
        type: String,
    },
});

module.exports = mongoose.model('Article', ArticleSchema);
