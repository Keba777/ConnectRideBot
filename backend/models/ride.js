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
  currentLocation: { type: String, required: true },
  destination: { type: String, required: true },
  status: { type: String, enum: validStatus, default: "requested" },
});

const Ride = mongoose.model("Ride", rideSchema);

function validateRide(ride) {
  const schema = Joi.object({
    user: Joi.string().required(),
    currentLocation: Joi.string().required(),
    destination: Joi.string().required(),
    status: Joi.string().valid(...validStatus),
  });

  return schema.validate(ride);
}

async function validateUserForRide(userId) {
  const user = await User.findById(userId);
  if (!user) return false;
  return user.role === "passenger";
}

export { Ride, validateRide, validateUserForRide };
