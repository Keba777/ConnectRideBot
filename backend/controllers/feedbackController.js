import { Feedback, validateFeedback } from "../models/feedback.js";

async function createFeedback(req, res) {
  try {
    console.log("Request Body:", req.body);
    const { error } = validateFeedback(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const feedback = new Feedback({
      ride: req.body.ride,
      passengerFeedback: req.body.passengerFeedback,
      driverFeedback: req.body.driverFeedback,
    });

    await feedback.save();
    res.status(201).send(feedback);
  } catch (err) {
    if (err.name === "MongoError" && err.code === 11000)
      return res.status(400).send("Feedback for this ride already exists.");
    res.status(500).send(err.message);
  }
}

async function getFeedback(req, res) {
  try {
    const rideId = req.params.rideId;
    const feedback = await Feedback.find({ ride: rideId });

    if (!feedback || feedback.length === 0)
      return res.status(404).send("No feedback found for the specified rideId");

    res.status(200).send(feedback);
  } catch (error) {
    res.status(500).send(error.message);
  }
}

async function updateFeedback(req, res) {
  try {
    const rideId = req.params.rideId;
    const { error } = validateFeedback(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const feedback = await Feedback.findOne({ ride: rideId });
    if (!feedback) return res.status(404).send("Feedback not found");

    feedback.ride = req.body.ride || feedback.ride;
    feedback.passengerFeedback =
      req.body.passengerFeedback || feedback.passengerFeedback;
    feedback.driverFeedback =
      req.body.driverFeedback || feedback.driverFeedback;

    await feedback.save();
    res.status(200).send(feedback);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createFeedback, getFeedback, updateFeedback };
