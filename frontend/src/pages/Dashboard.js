import { useState, useEffect } from "react";
import "./Dashboard.css";

import ActiveAgentsIcon from "../images/robot-icon.svg";
import MonthlySpendIcon from "../images/coin-icon.svg";
import JobsCompletedIcon from "../images/checkbox-icon.svg";
import SuccessRateIcon from "../images/up-arrow-icon.svg";

const BACKEND_URL = "http://localhost:8000";

function Dashboard() {
  const [stats, setStats] = useState({
    activeJobs: { running: 0, queued: 0, failed: 0 },
    monthlySpend: 0,
    jobsCompleted: 0,
    avgSuccessRate: 0,
  });

  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  const [recentJobs, setRecentJobs] = useState([
    {
      id: "JOB-9821",
      task: "Scrape product data from e-commerce site",
      agent: "DataScraper-AI",
      status: "completed",
      cost: 0.15,
      time: "2.1s",
    },
    {
      id: "JOB-9820",
      task: "Summarize research paper (15 pages)",
      agent: "SummarizeGPT",
      status: "completed",
      cost: 0.08,
      time: "1.9s",
    },
    {
      id: "JOB-9819",
      task: "Validate CSV data compliance",
      agent: "ValidatorPro",
      status: "processing",
      cost: 0.12,
      time: "—",
    },
  ]);

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        {/* Welcome Section */}
        <div className="welcome-section">
          <h1 className="page-title">Welcome to TUNDRA</h1>
          <p className="page-subtitle">Your AI agent marketplace</p>
        </div>

        {/* Summary Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon"><img src={ActiveAgentsIcon} alt="Active Jobs" /></div>
            <div className="stat-content">
              <h3>Active Jobs</h3>
              <div className="stat-value">
                {stats.activeJobs.running} running / {stats.activeJobs.queued} queued / {stats.activeJobs.failed} failed
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon"><img src={MonthlySpendIcon} alt="Monthly Spend" /></div>
            <div className="stat-content">
              <h3>Monthly Spend</h3>
              <div className="stat-value">${stats.monthlySpend.toFixed(2)}</div>
              <div className="stat-trend">+12% from last month</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon"><img src={JobsCompletedIcon} alt="Jobs Completed" /></div>
            <div className="stat-content">
              <h3>Jobs Completed</h3>
              <div className="stat-value">{stats.jobsCompleted}</div>
              <div className="stat-trend">This month</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon"><img src={SuccessRateIcon} alt="Avg. Success Rate" /></div>
            <div className="stat-content">
              <h3>Avg. Success Rate</h3>
              <div className="stat-value">{stats.avgSuccessRate}%</div>
              <div className="stat-trend success">+3% improvement</div>
            </div>
          </div>
        </div>

        {/* Autonomous Agents */}
        <div className="section">
          <h2 className="section-title">Autonomous Agents</h2>
          {loading ? (
            <p style={{ color: "var(--text-light)" }}>Loading agents...</p>
          ) : agents.length === 0 ? (
            <p style={{ color: "var(--text-light)" }}>No agents available</p>
          ) : (
            <div className="agent-feed">
              {agents.slice(0, 6).map((agent) => (
                <div key={agent._id || agent.id} className="agent-card">
                  <div className="agent-header">
                    <div>
                      <h3 className="agent-name">{agent.name}</h3>
                      <p className="agent-spec">
                        {agent.capabilities?.join(", ") || agent.specialization || "General AI"}
                      </p>
                    </div>
                    <span className={`status-badge status-${agent.status}`}>
                      {agent.status}
                    </span>
                  </div>
                  <div className="agent-metrics">
                    <div className="metric">
                      <span className="metric-label">Success Rate</span>
                      <span className="metric-value">
                        {agent.success_rate || agent.successRate || 0}%
                      </span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Price</span>
                      <span className="metric-value">
                        ${agent.pricing?.base_rate || agent.costPerJob || 0}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Jobs */}
        <div className="section">
          <h2 className="section-title">Recent Jobs</h2>
          <div className="jobs-table">
            <table>
              <thead>
                <tr>
                  <th>Job ID</th>
                  <th>Task</th>
                  <th>Agent</th>
                  <th>Status</th>
                  <th>Cost</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {recentJobs.map((job) => (
                  <tr key={job.id}>
                    <td className="job-id">{job.id}</td>
                    <td className="job-task">{job.task}</td>
                    <td>{job.agent}</td>
                    <td>
                      <span className={`job-status status-${job.status}`}>
                        {job.status}
                      </span>
                    </td>
                    <td>${job.cost}</td>
                    <td>{job.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
