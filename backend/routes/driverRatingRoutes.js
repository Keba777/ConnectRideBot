import { Router } from "express";
import { createDriverRating } from "../controllers/driverRatingController.js";

const router = Router();

router.post("/", createDriverRating);

export default router;
