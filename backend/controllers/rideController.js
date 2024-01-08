import { Ride, validateRide, validateUserForRide } from "../models/ride.js";

async function createRide(req, res) {
  try {
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

    await ride.save();
    res.status(201).send(ride);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

async function getRides(req, res) {
  try {
    const rides = await Ride.find().populate("user").populate("driver");
    const transformedRides = [];

    for (const ride of rides) {
      const transformedRide = {
        _id: ride._id,
        user: {
          telegramId: ride.user.telegramId,
          fullName: ride.user.fullName,
          phone: ride.user.phone,
        },
        driver: ride.driver
          ? {
              telegramId: ride.driver.telegramId,
              fullName: ride.driver.fullName,
              phone: ride.driver.phone,
            }
          : null,
        currentLocation: ride.currentLocation,
        destination: ride.destination,
        status: ride.status,
      };
      transformedRides.push(transformedRide);
    }

    res.status(200).send(transformedRides);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

async function updateRide(req, res) {
  try {
    const rideId = req.params.rideId;
    const { error } = validateRide(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const ride = await Ride.findById(rideId);
    if (!ride) return res.status(404).send("Ride not found");

    Object.assign(ride, req.body);

    await ride.save();
    res.status(200).send(ride);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

async function getRidesForUser(req, res) {
  const passengerId = req.params.passengerId;

  try {
    const rides = await Ride.find({ user: passengerId }).populate("driver");
    const transformedRides = rides.map((ride) => ({
      _id: ride._id,
      driver: ride.driver
        ? {
            telegramId: ride.driver.telegramId,
            fullName: ride.driver.fullName,
            phone: ride.driver.phone,
          }
        : null,
      currentLocation: ride.currentLocation,
      destination: ride.destination,
      status: ride.status,
    }));

    res.status(200).json(transformedRides);
  } catch (err) {
    res.status(500).send(err.message);
  }
}

export { createRide, getRides, updateRide, getRidesForUser };
