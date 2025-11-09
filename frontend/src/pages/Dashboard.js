import { useState, useEffect } from "react";
import "./Dashboard.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function Dashboard() {
  const [stats, setStats] = useState({
    activeJobs: { running: 0, queued: 0, failed: 0 },
    monthlySpend: 0,
    jobsCompleted: 0,
    avgSuccessRate: 0,
  });

  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recentJobs, setRecentJobs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setError(null);
      const [agentsRes, jobsRes] = await Promise.all([
        fetch(`${BACKEND_URL}/agents`),
        fetch(`${BACKEND_URL}/jobs`)
      ]);

      if (agentsRes.ok) {
        const agentsData = await agentsRes.json();
        const agentsList = agentsData.agents || agentsData;
        setAgents(agentsList.map(agent => ({
          ...agent,
          status: agent.balance > 0 ? "active" : "idle",
          success_rate: 95,
          pricing: { base_rate: agent.rate }
        })));
      } else {
        setError(`Failed to fetch agents: ${agentsRes.statusText}`);
      }

      if (jobsRes.ok) {
        const jobsData = await jobsRes.json();
        const jobsList = jobsData.jobs || jobsData;

        const completed = jobsList.filter(j => j.status === "completed").length;
        const inProgress = jobsList.filter(j => j.status === "in_progress").length;
        const open = jobsList.filter(j => j.status === "open").length;
        const failed = jobsList.filter(j => j.status === "failed").length;
        const claimed = jobsList.filter(j => j.status === "claimed").length;

        const totalSpend = jobsList
          .filter(j => j.status === "completed")
          .reduce((sum, j) => sum + (j.budget || 0), 0);

        setStats({
          activeJobs: {
            running: inProgress + claimed,
            queued: open,
            failed
          },
          monthlySpend: totalSpend,
          jobsCompleted: completed,
          avgSuccessRate: completed > 0 ? Math.round((completed / (completed + failed)) * 100) : 0
        });

        const recent = jobsList
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5)
          .map(job => ({
            id: job.job_id,
            task: job.task || job.goal || "No description",
            agent: job.provider_agent || "Pending",
            status: job.status,
            cost: job.budget || 0,
            time: job.completed_at ?
              `${Math.round((new Date(job.completed_at) - new Date(job.created_at)) / 1000)}s` :
              "In progress"
          }));

        setRecentJobs(recent);
      }

      setLoading(false);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      setError(`Error connecting to backend: ${error.message}`);
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <div className="welcome-section">
          <h1 className="page-title">Welcome to TUNDRA</h1>
          <p className="page-subtitle">Your AI agent marketplace</p>
        </div>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-content">
              <h3>Active Jobs</h3>
              <div className="stat-value">
                {stats.activeJobs.running} running / {stats.activeJobs.queued} queued / {stats.activeJobs.failed} failed
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-content">
              <h3>Monthly Spend</h3>
              <div className="stat-value">${stats.monthlySpend.toFixed(2)}</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-content">
              <h3>Jobs Completed</h3>
              <div className="stat-value">{stats.jobsCompleted}</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-content">
              <h3>Avg. Success Rate</h3>
              <div className="stat-value">{stats.avgSuccessRate}%</div>
            </div>
          </div>
        </div>

        <div className="section">
          <h2 className="section-title">Autonomous Agents</h2>
          {loading ? (
            <p style={{ color: "var(--text-light)" }}>Loading agents...</p>
          ) : agents.length === 0 ? (
            <p style={{ color: "var(--text-light)" }}>No agents available</p>
          ) : (
            <div className="agent-feed">
              {agents.slice(0, 6).map((agent) => (
                <div key={agent.name} className="agent-card">
                  <div className="agent-header">
                    <div>
                      <h3 className="agent-name">{agent.name}</h3>
                      <p className="agent-spec">
                        {agent.capabilities?.join(", ") || "General AI"}
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
                        {agent.success_rate || 0}%
                      </span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Price</span>
                      <span className="metric-value">
                        ${agent.pricing?.base_rate || agent.rate || 0}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

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
