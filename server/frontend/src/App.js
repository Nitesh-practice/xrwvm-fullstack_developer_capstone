import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register"; // Import Register component
import { Routes, Route } from "react-router-dom";
import Dealers from './components/Dealers/Dealers'; // Import Dealers component
import Dealer from "./components/Dealers/Dealer"; // Import Dealer component
import PostReview from "./components/Dealers/PostReview"; // Import PostReview component

function App() {
  return (
    <Routes>
      {/* Route for Login page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Route for Register page */}
      <Route path="/register" element={<Register />} />

      {/* Route for Dealers page */}
      <Route path="/dealers" element={<Dealers />} />

      {/* Route for Dealer-specific page with reviews */}
      <Route path="/dealer/:id" element={<Dealer />} />

      {/* Route for posting a review for a dealer */}
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;
