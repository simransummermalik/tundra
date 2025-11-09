import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";
import "./Profile.css";

function Profile() {
  const [user, setUser] = useState(null);
  const [stats] = useState({
    totalJobs: 342,
    totalSpent: 1247.50,
    avgSuccessRate: 87,
    memberSince: "November 2024"
  });

  const [activeJobs] = useState([
    { id: "JOB-9819", task: "Validate CSV data", status: "processing", progress: 45 },
    { id: "JOB-9818", task: "Analyze code repository", status: "queued", progress: 0 },
  ]);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
    });
  }, []);

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h1 className="page-title">Your Profile</h1>
        <p className="page-subtitle">Manage your TUNDRA account and view activity</p>

        {/* Account Info */}
        <div className="profile-section">
          <h2>Account Information</h2>
          <div className="profile-info">
            <div className="info-row">
              <span className="info-label">Email</span>
              <span className="info-value">{user?.email || "Loading..."}</span>
            </div>
            <div className="info-row">
              <span className="info-label">User ID</span>
              <span className="info-value code">{user?.id?.substring(0, 24) || "..."}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Member Since</span>
              <span className="info-value">{stats.memberSince}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Account Type</span>
              <span className="info-value">
                <span className="badge badge-info">Standard</span>
              </span>
            </div>
          </div>
        </div>

        {/* Usage Stats */}
        <div className="profile-section">
          <h2>Usage Statistics</h2>
          <div className="stats-grid-small">
            <div className="stat-card-small">
              <div className="stat-label-small">Total Jobs</div>
              <div className="stat-value-small">{stats.totalJobs}</div>
            </div>
            <div className="stat-card-small">
              <div className="stat-label-small">Total Spent</div>
              <div className="stat-value-small">${stats.totalSpent.toFixed(2)}</div>
            </div>
            <div className="stat-card-small">
              <div className="stat-label-small">Success Rate</div>
              <div className="stat-value-small">{stats.avgSuccessRate}%</div>
            </div>
          </div>
        </div>

        {/* Active Jobs */}
        <div className="profile-section">
          <h2>Active Jobs</h2>
          {activeJobs.length === 0 ? (
            <p className="empty-message">No active jobs</p>
          ) : (
            <div className="active-jobs-list">
              {activeJobs.map((job) => (
                <div key={job.id} className="active-job-item">
                  <div className="job-header">
                    <span className="job-id">{job.id}</span>
                    <span className={`status-badge status-${job.status}`}>
                      {job.status}
                    </span>
                  </div>
                  <p className="job-task">{job.task}</p>
                  {job.progress > 0 && (
                    <div className="progress-bar-small">
                      <div
                        className="progress-fill-small"
                        style={{ width: `${job.progress}%` }}
                      ></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Activity */}
        <div className="profile-section">
          <h2>Recent Activity</h2>
          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-icon success">✓</div>
              <div className="activity-content">
                <span className="activity-text">Job completed: Web scraping task</span>
                <span className="activity-time">2 hours ago</span>
              </div>
            </div>
            <div className="activity-item">
              <div className="activity-icon success">✓</div>
              <div className="activity-content">
                <span className="activity-text">Job completed: Text summarization</span>
                <span className="activity-time">5 hours ago</span>
              </div>
            </div>
            <div className="activity-item">
              <div className="activity-icon processing">⏳</div>
              <div className="activity-content">
                <span className="activity-text">Job started: Data validation</span>
                <span className="activity-time">1 day ago</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
