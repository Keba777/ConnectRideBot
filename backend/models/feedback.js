import mongoose from "mongoose";
import Joi from "joi";

const feedbackSchema = mongoose.Schema({
  feedback: { type: String, required: true },
});

const Feedback = mongoose.model("Feedback", feedbackSchema);

function validateFeedback(feedback) {
  const schema = Joi.object({
    feedback: Joi.string().required(),
  });

  return schema.validate(feedback);
}

export { Feedback, validateFeedback };
