import { useState, useEffect } from "react";
import "./Profile.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function Profile() {
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalSpent: 0,
    avgSuccessRate: 0,
    memberSince: "November 2024",
    balance: 0
  });

  const [activeJobs, setActiveJobs] = useState([]);

  useEffect(() => {
    fetchProfileData();
    const interval = setInterval(fetchProfileData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchProfileData = async () => {
    try {
      const [jobsRes, agentsRes] = await Promise.all([
        fetch(`${BACKEND_URL}/jobs`),
        fetch(`${BACKEND_URL}/agents`)
      ]);

      if (jobsRes.ok) {
        const jobsData = await jobsRes.json();
        const jobs = jobsData.jobs || jobsData;

        const completed = jobs.filter(j => j.status === "completed").length;
        const failed = jobs.filter(j => j.status === "failed").length;
        const totalSpent = jobs
          .filter(j => j.status === "completed")
          .reduce((sum, j) => sum + (j.budget || 0), 0);

        const pending = jobs.filter(j =>
          j.status === "open" || j.status === "claimed" || j.status === "in_progress"
        );

        setActiveJobs(pending.slice(0, 5).map(job => ({
          id: job.job_id,
          task: job.task || job.goal,
          status: job.status
        })));

        setStats({
          totalJobs: jobs.length,
          totalSpent,
          avgSuccessRate: completed > 0 ? Math.round((completed / (completed + failed)) * 100) : 0,
          memberSince: "November 2024",
          balance: 0
        });
      }

      if (agentsRes.ok) {
        const agentsData = await agentsRes.json();
        const agentsList = agentsData.agents || agentsData;
        const orchestrator = agentsList.find(a => a.name === "OrchestratorAgent");
        if (orchestrator) {
          setStats(prev => ({ ...prev, balance: orchestrator.balance || 0 }));
        }
      }
    } catch (error) {
      console.error("Error fetching profile data:", error);
    }
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h1 className="page-title">Your Profile</h1>
        <p className="page-subtitle">Manage your TUNDRA account and view activity</p>

        <div className="profile-section">
          <h2>Account Information</h2>
          <div className="profile-info">
            <div className="info-row">
              <span className="info-label">Account</span>
              <span className="info-value">OrchestratorAgent</span>
            </div>
            <div className="info-row">
              <span className="info-label">Credits Balance</span>
              <span className="info-value">${stats.balance.toFixed(2)}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Member Since</span>
              <span className="info-value">{stats.memberSince}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Account Type</span>
              <span className="info-value">
                <span className="badge badge-info">Requester</span>
              </span>
            </div>
          </div>
        </div>

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
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Profile;
