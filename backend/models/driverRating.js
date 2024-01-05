import mongoose from "mongoose";
import Joi from "joi";

const driverRatingSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  rating: { type: Number, required: true, min: 1, max: 5 },
  feedback: { type: String },
});
const DriverRating = mongoose.model("DriverRating", driverRatingSchema);

function validateDriverRating(driverRating) {
  const schema = Joi.object({
    user: Joi.string().required(),
    rating: Joi.number().required().min(1).max(5),
    feedback: Joi.string(),
  });

  return schema.validate(driverRating);
}

export { DriverRating, validateDriverRating };
