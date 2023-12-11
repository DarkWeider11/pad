const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const interactionSchema = new Schema({
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
    enum: ['view', 'like', 'add-to-favorites'],
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
});

// unique interactions
interactionSchema.index(
    { userId: 1, contentId: 1, interactionType: 1 }, 
    { unique: true }
  );

const Interaction = mongoose.model('Interaction', interactionSchema);

module.exports = Interaction;