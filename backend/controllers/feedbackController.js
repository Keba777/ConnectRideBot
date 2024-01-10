import { Feedback, validateFeedback } from "../models/feedback.js";

async function createFeedback(req, res) {
  try {
    const { error } = validateFeedback(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const feedback = new Feedback({
      feedback: req.body.feedback,
    });

    await feedback.save();
    res.status(201).send(feedback);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createFeedback };
