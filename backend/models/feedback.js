import mongoose from "mongoose";
import Joi from "joi";

const feedbackSchema = mongoose.Schema({
  ride: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Ride",
    required: true,
    unique: true,
  },
  passengerFeedback: {
    rating: { type: Number, default: null, min: 1, max: 5 },
    feedback: { type: String, default: null },
  },
  driverFeedback: {
    rating: { type: Number, default: null, min: 1, max: 5 },
    feedback: { type: String, default: null },
  },
});

const Feedback = mongoose.model("Feedback", feedbackSchema);

function validateFeedback(feedback) {
  const schema = Joi.object({
    ride: Joi.string().regex(/^[0-9a-fA-F]{24}$/),
    passengerFeedback: Joi.object({
      rating: Joi.number().min(1).max(5).allow(null),
      feedback: Joi.string().allow(null),
    }).default(null),
    driverFeedback: Joi.object({
      rating: Joi.number().min(1).max(5).allow(null),
      feedback: Joi.string().allow(null),
    }).default(null),
  });

  return schema.validate(feedback);
}

export { Feedback, validateFeedback };
