import { Router } from "express";
import { createUserRating } from "../controllers/userRatingController.js";

const router = Router();

router.post("/", createUserRating);

export default router;
