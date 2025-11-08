//src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./login";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Marketplace from "./pages/Marketplace";
import Profile from "./pages/Profile";
import Prompt from "./pages/Prompt";
import "./App.css";


function App() {
  return (
    <div className="app-root">
      <Login />
    </div>
  );
}

export default App;