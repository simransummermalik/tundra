import { useState } from "react";
import { supabase } from "../supabaseClient";
import "./Settings.css";

function Settings() {
  const [apiKey, setApiKey] = useState("tundra_sk_1234567890abcdef");
  const [notifications, setNotifications] = useState({
    jobComplete: true,
    jobFailed: true,
    weeklyReport: false,
  });

  const handleRegenerateKey = () => {
    const newKey = `tundra_sk_${Math.random().toString(36).substring(2, 15)}`;
    setApiKey(newKey);
    alert("New API key generated!");
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
          <h2>API Key</h2>
          <p className="section-description">
            Use this key to authenticate API requests and CLI access
          </p>
          <div className="api-key-box">
            <code>{apiKey}</code>
            <button className="btn btn-secondary" onClick={handleRegenerateKey}>
              Regenerate
            </button>
          </div>
          <p className="warning-text">
            Keep your API key secret. Never share it or commit it to version control.
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
