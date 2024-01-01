import mongoose from "mongoose";
import Joi from "joi";

const validRoles = ["driver", "passenger"];

const User = mongoose.model("User", {
  telegramId: { type: Number, unique: true },
  fullName: String,
  phone: String,
  role: { type: String, enum: validRoles },
});

function validateUser(user) {
  const schema = Joi.object({
    telegramId: Joi.number().integer().required(),
    fullName: Joi.string().required(),
    phone: Joi.string().required(),
    role: Joi.string()
      .valid(...validRoles)
      .required(),
  });

  return schema.validate(user);
}

export { User, validateUser };
