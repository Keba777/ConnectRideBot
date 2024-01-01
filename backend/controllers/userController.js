import { User, validateUser } from "../models/user.js";

const registerUser = async (req, res) => {
  try {
    const { error } = validateUser(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    let user = await User.findOne({ telegramId: req.body.telegramId });
    if (user) return res.status(400).send("User already registered.");

    user = new User({
      telegramId: req.body.telegramId,
      fullName: req.body.fullName,
      phone: req.body.phone,
      role: req.body.role,
    });

    await user.save();

    res.send(user);
  } catch (error) {
    console.error("Error registering user:", error);
    res.status(500).send("Internal Server Error");
  }
};

const getUser = async (req, res) => {
  try {
    const telegramId = req.params.telegramId;
    const user = await User.findOne({ telegramId });

    if (!user) {
      return res
        .status(404)
        .send({ success: false, message: "User not found" });
    }

    return res.send({ success: true, user });
  } catch (error) {
    console.error("Error fetching user:", error);
    res.status(500).send({ success: false, message: "Internal Server Error" });
  }
};

export { registerUser, getUser };
