import express from "express";
import {
  registerUser,
  getUser,
  updateUser,
} from "../controllers/userController.js";

const router = express.Router();

router.post("/", registerUser);
router.get("/:telegramId", getUser);
router.put("/:telegramId", updateUser);

export default router;
