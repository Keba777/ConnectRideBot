import { UserRating, validateUserRating } from "../models/userRating.js";

async function createUserRating(req, res) {
  const { error } = validateUserRating(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  const userRating = UserRating({
    ride: req.body.ride,
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
