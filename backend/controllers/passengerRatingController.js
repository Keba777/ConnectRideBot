import {
  PassengerRating,
  validatePassengerRating,
} from "../models/passengerRating.js";
import { validateUserForRide } from "../models/ride.js";

async function createPassengerRating(req, res) {
  const { error } = validatePassengerRating(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  const isValidUser = await validateUserForRide(req.body.user);
  if (!isValidUser)
    return res.status(403).send("Invalid user or user is not a passenger.");

  const passengerRating = PassengerRating({
    user: req.body.user,
    rating: req.body.rating,
    feedback: req.body.feedback,
  });

  try {
    await passengerRating.save();
    res.status(201).send(passengerRating);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createPassengerRating };
