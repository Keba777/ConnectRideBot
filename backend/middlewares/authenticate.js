// middleware/authenticate.js

import { User } from "../models/user.js";

async function authenticateUser(req, res, next) {
  try {
    const userId = req.params.userId;

    const user = await User.findById(userId);

    if (user && user.role === "driver") {
      req.user = user;
      next();
    } else {
      res.status(401).send("Unauthorized");
    }
  } catch (err) {
    console.error(err);
    res.status(500).send("Internal Server Error");
  }
}

export { authenticateUser };
