import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./login";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Marketplace from "./pages/Marketplace";
import Profile from "./pages/Profile";
import Jobs from "./pages/Jobs";
import Transactions from "./pages/Transactions";
import Settings from "./pages/Settings";
import { supabase } from "./supabaseClient";
import "./App.css";

const BACKEND_URL = "http://localhost:8000";

function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  // Auto-generate API key for user on login
  const ensureApiKey = async (user) => {
    try {
      const response = await fetch(`${BACKEND_URL}/auth/get-or-create-key`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: user.email,
          user_id: user.id,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store the API key if it's a new one (not masked)
        if (!data.api_key.includes("•")) {
          localStorage.setItem("tundra_api_key", data.api_key);
        }
      }
    } catch (error) {
      console.error("Failed to ensure API key:", error);
    }
  };

  useEffect(() => {
    // Check current session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      if (session?.user) {
        ensureApiKey(session.user);
      }
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session?.user) {
        ensureApiKey(session.user);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <h2>TUNDRA</h2>
        <p>Loading...</p>
      </div>
    );
  }

  if (!session) {
    return <Login />;
  }

  return (
    <Router>
      <div className="app-root">
        <Navbar session={session} />
        <div className="app-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/agents" element={<Marketplace />} />
            <Route path="/jobs" element={<Jobs />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
