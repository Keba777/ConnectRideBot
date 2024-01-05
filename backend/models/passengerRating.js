import mongoose from "mongoose";
import Joi from "joi";

const passengerRatingSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  rating: { type: Number, required: true, min: 1, max: 5 },
  feedback: { type: String },
});
const PassengerRating = mongoose.model(
  "PassengerRating",
  passengerRatingSchema
);

function validatePassengerRating(passengerRating) {
  const schema = Joi.object({
    user: Joi.string().required(),
    rating: Joi.number().required().min(1).max(5),
    feedback: Joi.string(),
  });

  return schema.validate(passengerRating);
}

export { PassengerRating, validatePassengerRating };
