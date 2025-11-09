import { useState, useEffect } from "react";
import "./Dashboard.css";

import ActiveAgentsIcon from "../images/robot-icon.svg";
import MonthlySpendIcon from "../images/coin-icon.svg";
import JobsCompletedIcon from "../images/checkbox-icon.svg";
import SuccessRateIcon from "../images/up-arrow-icon.svg";
import TrustScoreIcon from "../images/trust-icon.svg";

function Dashboard() {
  // Placeholder data - replace with API calls later
  const [stats, setStats] = useState({
    activeAgents: { running: 2, idle: 3, disabled: 1 },
    monthlySpend: 1247.50,
    jobsCompleted: 342,
    avgSuccessRate: 87,
    trustScore: 92,
  });

  const [agents, setAgents] = useState([
    {
      id: 1,
      name: "DataScraper-AI",
      specialization: "Web Scraping",
      status: "active",
      speed: "2.3s",
      successRate: 94,
      costPerJob: 0.15,
    },
    {
      id: 2,
      name: "SummarizeGPT",
      specialization: "Text Summarization",
      status: "active",
      speed: "1.8s",
      successRate: 91,
      costPerJob: 0.08,
    },
    {
      id: 3,
      name: "ValidatorPro",
      specialization: "Data Validation",
      status: "idle",
      speed: "3.1s",
      successRate: 89,
      costPerJob: 0.12,
    },
    {
      id: 4,
      name: "CodeReview-AI",
      specialization: "Code Analysis",
      status: "idle",
      speed: "4.5s",
      successRate: 85,
      costPerJob: 0.22,
    },
  ]);

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
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Monitor your AI agent activity and performance</p>

        {/* Summary Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon"><img src={ActiveAgentsIcon} alt="Active Agents" /></div>
            <div className="stat-content">
              <h3>Active Agents</h3>
              <div className="stat-value">
                {stats.activeAgents.running} running / {stats.activeAgents.idle} idle / {stats.activeAgents.disabled} disabled
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

          <div className="stat-card">
            <div className="stat-icon"><img src={TrustScoreIcon} alt="Trust Score" /></div>
            <div className="stat-content">
              <h3>Trust Score</h3>
              <div className="stat-value">{stats.trustScore}/100</div>
              <div className="stat-trend success">Excellent</div>
            </div>
          </div>
        </div>

        {/* Live Agent Feed */}
        <div className="section">
          <h2 className="section-title">Live Agent Feed</h2>
          <div className="agent-feed">
            {agents.map((agent) => (
              <div key={agent.id} className="agent-card">
                <div className="agent-header">
                  <div>
                    <h3 className="agent-name">{agent.name}</h3>
                    <p className="agent-spec">{agent.specialization}</p>
                  </div>
                  <span className={`status-badge status-${agent.status}`}>
                    {agent.status}
                  </span>
                </div>
                <div className="agent-metrics">
                  <div className="metric">
                    <span className="metric-label">Speed</span>
                    <span className="metric-value">{agent.speed}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Success Rate</span>
                    <span className="metric-value">{agent.successRate}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Cost/Job</span>
                    <span className="metric-value">${agent.costPerJob}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
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
