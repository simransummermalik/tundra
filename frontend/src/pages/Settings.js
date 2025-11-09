import { useState } from "react";
import "./Settings.css";

function Settings() {
  const [settings, setSettings] = useState({
    notifications: true,
    autoAccept: false,
    maxBudget: 100,
  });

  const handleSettingChange = (key, value) => {
    setSettings({ ...settings, [key]: value });
  };

  const handleSave = () => {
    alert("Settings saved successfully");
  };

  return (
    <div className="settings-page">
      <div className="settings-container">
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Configure your TUNDRA preferences</p>

        <div className="settings-section">
          <h2>General Settings</h2>
          <div className="setting-item">
            <div className="setting-info">
              <label>Enable Notifications</label>
              <p className="setting-description">
                Receive notifications when jobs are completed
              </p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifications}
              onChange={(e) =>
                handleSettingChange("notifications", e.target.checked)
              }
            />
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>Auto-Accept Jobs</label>
              <p className="setting-description">
                Automatically accept jobs within budget
              </p>
            </div>
            <input
              type="checkbox"
              checked={settings.autoAccept}
              onChange={(e) =>
                handleSettingChange("autoAccept", e.target.checked)
              }
            />
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>Maximum Budget Per Job</label>
              <p className="setting-description">
                Set the maximum amount you're willing to spend per job
              </p>
            </div>
            <input
              type="number"
              value={settings.maxBudget}
              onChange={(e) =>
                handleSettingChange("maxBudget", parseInt(e.target.value))
              }
              min="0"
              className="budget-input"
            />
          </div>
        </div>

        <button className="btn btn-primary" onClick={handleSave}>
          Save Settings
        </button>
      </div>
    </div>
  );
}

export default Settings;
