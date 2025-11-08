// src/Login.js
import React, { useState } from "react";
import "./login.css";
import logo from "./assets/logo.png";
import { supabase } from "./supabaseClient";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    setLoading(false);

    if (error) {
      setError(error.message);
    } else if (data.session) {
      setSuccess(true);
      console.log("Signed in:", data.session);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <img src={logo} alt="TUNDRA" className="login-logo" />
          <h1>TUNDRA</h1>
          <p className="subtitle">Where intelligence learns to self-govern.</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <label>Email</label>
          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Log In"}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">Login successful ✅</p>}
      </div>
    </div>
  );
};

export default Login;
