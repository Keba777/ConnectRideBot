import mongoose from "mongoose";
import Joi from "joi";
import { User } from "./user.js";

const validStatus = ["requested", "accepted", "completed", "canceled"];

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
