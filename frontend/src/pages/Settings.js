import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";
import "./Settings.css";

const BACKEND_URL = "http://localhost:8000"; // Change this when deployed

function Settings() {
  const [apiKey, setApiKey] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [notifications, setNotifications] = useState({
    jobComplete: true,
    jobFailed: true,
    weeklyReport: false,
  });

  useEffect(() => {
    // Check if user already has an API key (you'd fetch this from your DB)
    const savedKey = localStorage.getItem("tundra_api_key");
    if (savedKey) {
      setApiKey(savedKey);
    }
  }, []);

  const handleGenerateKey = async () => {
    setLoading(true);
    setError("");

    try {
      // Get current user from Supabase
      const { data: { user } } = await supabase.auth.getUser();

      if (!user) {
        setError("Not authenticated");
        return;
      }

      // Call backend to generate API key
      const response = await fetch(`${BACKEND_URL}/auth/generate-key`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: user.email,
          user_id: user.id,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate API key");
      }

      const data = await response.json();
      setApiKey(data.api_key);
      setShowKey(true);

      // Save to localStorage
      localStorage.setItem("tundra_api_key", data.api_key);

      alert("API key generated! Make sure to copy it now - it won't be shown again.");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = () => {
    alert("Settings saved! (This will connect to backend later)");
  };

  return (
    <div className="settings-page">
      <div className="settings-container">
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Manage your TUNDRA account and preferences</p>

        {/* API Key Section */}
        <div className="settings-section">
          <h2>API Key for CLI</h2>
          <p className="section-description">
            Use this key to authenticate with the TUNDRA CLI
          </p>

          {error && <p className="error-message">{error}</p>}

          {!apiKey ? (
            <div>
              <p>You don't have an API key yet. Generate one to use the CLI.</p>
              <button
                className="btn btn-primary"
                onClick={handleGenerateKey}
                disabled={loading}
              >
                {loading ? "Generating..." : "Generate API Key"}
              </button>
            </div>
          ) : (
            <div className="api-key-box">
              <code>{showKey ? apiKey : "tundra_sk_••••••••••••••••"}</code>
              <button
                className="btn btn-secondary"
                onClick={() => setShowKey(!showKey)}
              >
                {showKey ? "Hide" : "Show"}
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  navigator.clipboard.writeText(apiKey);
                  alert("API key copied to clipboard!");
                }}
              >
                Copy
              </button>
            </div>
          )}

          <div className="cli-instructions">
            <h3>How to use with CLI:</h3>
            <pre><code>tundra login --api-base {BACKEND_URL} --key {apiKey ? "YOUR_API_KEY" : "your_api_key_here"}</code></pre>
          </div>

          <p className="warning-text">
            ⚠️ Keep your API key secret. Never share it or commit it to version control.
          </p>
        </div>

        {/* Notification Settings */}
        <div className="settings-section">
          <h2>Notifications</h2>
          <p className="section-description">Choose what updates you want to receive</p>

          <div className="notification-options">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={notifications.jobComplete}
                onChange={(e) =>
                  setNotifications({ ...notifications, jobComplete: e.target.checked })
                }
              />
              <span>Job completion notifications</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={notifications.jobFailed}
                onChange={(e) =>
                  setNotifications({ ...notifications, jobFailed: e.target.checked })
                }
              />
              <span>Job failure alerts</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={notifications.weeklyReport}
                onChange={(e) =>
                  setNotifications({ ...notifications, weeklyReport: e.target.checked })
                }
              />
              <span>Weekly usage reports</span>
            </label>
          </div>
        </div>

        {/* Budget Limits */}
        <div className="settings-section">
          <h2>Spending Limits</h2>
          <p className="section-description">Set maximum spending limits for safety</p>

          <div className="form-row">
            <div className="form-group">
              <label>Daily Limit ($)</label>
              <input type="number" defaultValue="100" min="0" step="10" />
            </div>
            <div className="form-group">
              <label>Monthly Limit ($)</label>
              <input type="number" defaultValue="1000" min="0" step="50" />
            </div>
          </div>
        </div>

        {/* Region Preferences */}
        <div className="settings-section">
          <h2>Region Preferences</h2>
          <p className="section-description">Prioritize agents in specific regions for lower latency</p>

          <div className="form-group">
            <label>Preferred Region</label>
            <select defaultValue="us-east">
              <option value="auto">Auto-select</option>
              <option value="us-east">US East</option>
              <option value="us-west">US West</option>
              <option value="eu-west">EU West</option>
              <option value="asia-pacific">Asia Pacific</option>
            </select>
          </div>
        </div>

        {/* Save Button */}
        <div className="settings-actions">
          <button className="btn btn-primary" onClick={handleSaveSettings}>
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}

export default Settings;
