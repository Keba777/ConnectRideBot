import { Ride, validateRide, validateUserForRide } from "../models/ride.js";
import { User } from "../models/user.js";

async function createRide(req, res) {
  const { error } = validateRide(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  const isValidUser = await validateUserForRide(req.body.user);
  if (!isValidUser)
    return res.status(403).send("Invalid user or user is not a passenger.");

  const ride = new Ride({
    user: req.body.user,
    currentLocation: req.body.currentLocation,
    destination: req.body.destination,
    status: req.body.status,
  });

  try {
    await ride.save();
    res.status(201).send(ride);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

async function getRides(req, res) {
  try {
    const rides = await Ride.find();
    const transformedRides = [];

    for (const ride of rides) {
      const user = await User.findById(ride.user);
      if (user) {
        const transformedRide = {
          user: {
            fullName: user.fullName,
            phone: user.phone,
          },
          currentLocation: ride.currentLocation,
          destination: ride.destination,
          status: ride.status,
        };
        transformedRides.push(transformedRide);
      }
    }

    res.status(200).send(transformedRides);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createRide, getRides };
