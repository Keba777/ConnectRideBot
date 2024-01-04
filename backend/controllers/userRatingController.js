import { UserRating, validateUserRating } from "../models/userRating.js";
import { validateUserForRide } from "../models/ride.js";

async function createUserRating(req, res) {
  const { error } = validateUserRating(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  const isValidUser = await validateUserForRide(req.body.user);
  if (!isValidUser)
    return res.status(403).send("Invalid user or user is not a passenger.");

  const userRating = UserRating({
    user: req.body.user,
    rating: req.body.rating,
    feedback: req.body.feedback,
  });

  try {
    await userRating.save();
    res.status(201).send(userRating);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createUserRating };
