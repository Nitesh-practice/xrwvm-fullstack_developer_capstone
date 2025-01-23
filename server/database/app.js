const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });

} catch (error) {
  res.status(500).json({ error: 'Error fetching documents' });
}

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealerships.find();  // Fetch all dealers
    res.json(dealers);  // Return all dealers in JSON format
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// Express route to fetch dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
  const { state } = req.params;  // Extract the state parameter from the URL
  try {
    const dealers = await Dealerships.find({ state: state });  // Fetch dealers by state
    if (dealers.length === 0) {
      return res.status(404).json({ message: `No dealers found in state: ${state}` });
    }
    res.json(dealers);  // Return the dealers from the specified state
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// Express route to fetch dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
  const { id } = req.params;  // Extract the dealer's ID from the URL
  try {
    const dealer = await Dealerships.findById(id);  // Find the dealer by ID
    if (!dealer) {
      return res.status(404).json({ message: `Dealer with ID ${id} not found` });
    }
    res.json(dealer);  // Return the dealer's details
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = documents[0]['id'] + 1;

  const review = new Reviews({
    "id": new_id,
    "name": data['name'],
    "dealership": data['dealership'],
    "review": data['review'],
    "purchase": data['purchase'],
    "purchase_date": data['purchase_date'],
    "car_make": data['car_make'],
    "car_model": data['car_model'],
    "car_year": data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
