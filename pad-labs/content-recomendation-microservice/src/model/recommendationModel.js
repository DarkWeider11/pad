const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const recommendationSchema = new Schema ({
    recommendationId: {
        type: String,
        required: true
    },
    userId: {
        type: String,
        required: true
    },
    recommendations: {
        type: [String],
        required: true
    }
})

const Recommendation = mongoose.model('Recommendation', recommendationSchema);

module.exports = Recommendation;