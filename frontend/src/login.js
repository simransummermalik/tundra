// src/Login.js
import React, { useState } from "react";
import "./login.css";
import logo from "./assets/logo.png"; // change if your file name is different

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // this does nothing right now ... plug Supabase here later
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("login attempt", { email, password });
    // TODO: supabase.auth.signInWithPassword(...)
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <img src={logo} alt="TUNDRA" className="login-logo" />
          <h1>TUNDRA</h1>
          <p className="subtitle">put a subtitle here</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className="login-button">
            Log In
          </button>
        </form>

        <p className="helper-text">
          Supabase auth will go here — this is just the UI.
        </p>
      </div>
    </div>
  );
};

export default Login;
