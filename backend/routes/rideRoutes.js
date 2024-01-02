import { Router } from "express";
import { createRide, getRides } from "../controllers/rideController.js";
import { authenticateUser } from "../middlewares/authenticate.js";

const router = Router();

router.post("/", createRide);
router.get("/:userId", authenticateUser, getRides);

export default router;
