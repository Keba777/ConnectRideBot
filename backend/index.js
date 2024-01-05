import express from "express";
import cors from "cors";
import connectDB from "./db/db.js";
import userRoutes from "./routes/userRoutes.js";
import rideRoutes from "./routes/rideRoutes.js";
import passengerRatingRoutes from "./routes/passengerRatingRoutes.js";

const app = express();

connectDB();

app.use(cors());
app.use(express.json());

app.use("/api/users", userRoutes);
app.use("/api/rides", rideRoutes);
app.use("/api/passengerRatings", passengerRatingRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Listening at port ${PORT}`));
