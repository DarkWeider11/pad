const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const contentSchema = Schema({
    contentId: {
        type: String, 
        required: true
    },
    title: {
        type: String,
        required: true
    },
    rating :{
        type: Number,
        required: true
    },
    genre: {
        type: [String], 
        required: true
    },
    cast: {
        type: [String], 
        required: true
    },
    release_year: {
        type: Number,
        required: true
    }
});

const Content = mongoose.model('Content', contentSchema);
module.exports = Content;