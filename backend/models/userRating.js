import mongoose from "mongoose";
import Joi from "joi";

const userRatingSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  rating: { type: Number, required: true, min: 1, max: 5 },
  feedback: { type: String },
});
const UserRating = mongoose.model("UserRating", userRatingSchema);

function validateUserRating(userRating) {
  const schema = Joi.object({
    user: Joi.string().required(),
    rating: Joi.number().required().min(1).max(5),
    feedback: Joi.string(),
  });

  return schema.validate(userRating);
}

export { UserRating, validateUserRating };
