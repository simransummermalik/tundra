import React, { useState } from "react";
import "./login.css";
import logo from "./assets/logo.png";
import videoBackground from "./assets/tundralogin.mp4";
import { supabase } from "./supabaseClient";

const Login = () => {
  const [mode, setMode] = useState("signin"); // "signin" or "signup"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      if (mode === "signin") {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (error) throw error;
        setMessage("Signed in successfully");
        console.log("SESSION:", data.session);
      } else {
        // signup
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
        });
        if (error) throw error;
        setMessage("Account created! Check your email (if confirmation is on).");
        console.log("SIGNUP:", data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <video
        autoPlay
        loop
        muted
        playsInline
        className="video-background"
      >
        <source src={videoBackground} type="video/mp4" />
      </video>
      <div className="login-card">
        <div className="login-header">
          <img src={logo} alt="TUNDRA" className="login-logo" />
          <h1>TUNDRA</h1>
          <p className="subtitle">Where intelligence learns to self-govern.</p>
        </div>

        <div className="toggle-row">
          <button
            className={mode === "signin" ? "toggle-btn active" : "toggle-btn"}
            onClick={() => {
              setMode("signin");
              setError("");
              setMessage("");
            }}
          >
            Sign In
          </button>
          <button
            className={mode === "signup" ? "toggle-btn active" : "toggle-btn"}
            onClick={() => {
              setMode("signup");
              setError("");
              setMessage("");
            }}
          >
            Sign Up
          </button>
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

          <button type="submit" className="login-button" disabled={loading}>
            {loading
              ? mode === "signin"
                ? "Signing in..."
                : "Creating account..."
              : mode === "signin"
              ? "Sign In"
              : "Sign Up"}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
        {message && <p className="success-message">{message}</p>}

        <p className="helper-text">
          {mode === "signin"
            ? "Don't have an account? Click Sign Up."
            : "Already have an account? Click Sign In."}
        </p>
      </div>
    </div>
  );
};

export default Login;
