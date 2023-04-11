const mongoose = require('mongoose');

const JobSchema = mongoose.Schema({
    querys: {
        type: [],
        default: [],
    },
    used: {
        type: Boolean,
        default: false,
    },
    user: {
        type: String,
    }
});

module.exports = mongoose.model('Job', JobSchema);
