import React from "react";
import "./Home.css";
//import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-page">
      <div className="hero">
        <h1>TUNDRA</h1>
        <p>Where Intelligence Learns to Self-Govern</p>
        <div className="hero-buttons">
          <Link to="/marketplace" className="btn">Browse Agents</Link>
          <Link to="/prompt" className="btn">Create Job</Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
