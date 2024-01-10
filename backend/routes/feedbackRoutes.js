import { Router } from "express";
import {
  createFeedback,
  getFeedback,
  updateFeedback,
} from "../controllers/feedbackController.js";

const router = Router();

router.post("/", createFeedback);
router.get("/:rideId", getFeedback);
router.put("/:rideId", updateFeedback);

export default router;
