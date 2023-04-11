const mongoose = require('mongoose');

const QuerySchema = mongoose.Schema({
    query: {
        type: String,
    },
    used: {
        type: Boolean,
        default: false,
    },
    articles: {
        type: [],
    },
    userId: {
        type: String,
    },
    jobId:{
        type: String,
    },
    state:{
        type: String,
    }
});

module.exports = mongoose.model('Query', QuerySchema);
