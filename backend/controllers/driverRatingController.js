import { DriverRating, validateDriverRating } from "../models/driverRating.js";

async function createDriverRating(req, res) {
  const { error } = validateDriverRating(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  const driverRating = DriverRating({
    user: req.body.user,
    rating: req.body.rating,
    feedback: req.body.feedback,
  });

  try {
    await driverRating.save();
    res.status(201).send(driverRating);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createDriverRating };
