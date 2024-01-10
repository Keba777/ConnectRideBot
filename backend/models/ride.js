import mongoose from "mongoose";
import Joi from "joi";
import { User } from "./user.js";

const validStatus = ["requested", "accepted", "completed", "canceled"];

const feedbackSchema = {
  rating: { type: Number, default: null, min: 1, max: 5 },
  review: { type: String, default: null },
};

const rideSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  driver: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    default: null,
  },
  currentLocation: { type: String, required: true },
  destination: { type: String, required: true },
  status: { type: String, enum: validStatus, default: "requested" },
  fare: { type: Number, default: null },
  userFeedback: { type: feedbackSchema, default: {} },
  driverFeedback: { type: feedbackSchema, default: {} },
});

const Ride = mongoose.model("Ride", rideSchema);

function validateRide(ride) {
  const schema = Joi.object({
    user: Joi.string(),
    driver: Joi.string().allow(null),
    currentLocation: Joi.string(),
    destination: Joi.string(),
    status: Joi.string().valid(...validStatus),
    fare: Joi.number().allow(null),
    userFeedback: Joi.object({
      rating: Joi.number().allow(null).min(1).max(5),
      review: Joi.string().allow(null),
    }),
    driverFeedback: Joi.object({
      rating: Joi.number().allow(null).min(1).max(5),
      review: Joi.string().allow(null),
    }),
  });

  return schema.validate(ride);
}

async function validateUserForRide(userId) {
  const user = await User.findById(userId);
  if (!user) return false;
  return user.role === "passenger";
}

async function validateUserAsDriver(userId) {
  const user = await User.findById(userId);
  if (!user) return false;
  return user.role === "driver";
}

export { Ride, validateRide, validateUserForRide, validateUserAsDriver };
