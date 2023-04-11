const mongoose = require('mongoose');

const ArticleUploadedSchema = mongoose.Schema({
    filename: {
        type: String,
    },
    used: {
        type: Boolean,
        default: false,
    },
    userId: {
        type: String,
    },
});

module.exports = mongoose.model('ArticleUploaded', ArticleUploadedSchema);
