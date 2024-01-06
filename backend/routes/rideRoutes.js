import { Router } from "express";
import {
  createRide,
  getRides,
  updateRide,
} from "../controllers/rideController.js";
import { authenticateUser } from "../middlewares/authenticate.js";

const router = Router();

router.post("/", createRide);
router.get("/:userId", authenticateUser, getRides);
router.put("/:rideId", updateRide);

export default router;
