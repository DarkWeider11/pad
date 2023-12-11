const mongoose = require('mongoose');

const commentInteractionSchema = new mongoose.Schema({
    userId: {
        type: String,
        required: true
    },
    contentId: {
        type: String,
        required: true
    },
    interactionType: {
        type: String,
        required: true
    },
    timestamp: {
        type: Date,
        default: Date.now
    },
    comment:{
        type: String,
        required: true
    }
});

const CommentInteraction = mongoose.model('CommentInteraction', commentInteractionSchema);

module.exports = CommentInteraction;
