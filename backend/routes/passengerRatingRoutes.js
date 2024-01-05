import { Router } from "express";
import { createPassengerRating } from "../controllers/passengerRatingController.js";

const router = Router();

router.post("/", createPassengerRating);

export default router;
