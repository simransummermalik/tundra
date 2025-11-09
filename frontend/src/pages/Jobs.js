import { useState, useEffect } from "react";
import "./Jobs.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function Jobs() {
  const [activeTab, setActiveTab] = useState("new");
  const [newJobForm, setNewJobForm] = useState({
    task: "",
    goal: "",
    payload: {}
  });
  const [pendingJobs, setPendingJobs] = useState([]);
  const [completedJobs, setCompletedJobs] = useState([]);
  const [failedJobs, setFailedJobs] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchJobs = async () => {
    try {
      setError(null);
      const response = await fetch(`${BACKEND_URL}/jobs`);
      if (response.ok) {
        const data = await response.json();
        const jobs = data.jobs || data;

        setPendingJobs(jobs.filter(j =>
          j.status === "open" || j.status === "claimed" || j.status === "in_progress"
        ));

        setCompletedJobs(jobs.filter(j => j.status === "completed"));
        setFailedJobs(jobs.filter(j => j.status === "failed"));
      } else {
        setError(`Failed to fetch jobs: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error fetching jobs:", error);
      setError(`Error connecting to backend: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleNewJobSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await fetch(`${BACKEND_URL}/submit_job`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task: newJobForm.task,
          goal: newJobForm.goal || newJobForm.task,
          payload: {}
        }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Job submitted successfully! Job ID: ${data.job_id}`);
        setNewJobForm({ task: "", goal: "", payload: {} });
        fetchJobs();
        setActiveTab("pending");
      } else {
        const error = await response.text();
        alert(`Failed to submit job: ${error}`);
      }
    } catch (error) {
      console.error("Error submitting job:", error);
      alert(`Error submitting job: ${error.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="jobs-page">
      <div className="jobs-container">
        <h1 className="page-title">Job Management</h1>
        <p className="page-subtitle">Create, track, and manage your AI agent jobs</p>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="tabs">
          {["new", "pending", "completed", "failed"].map((tab) => (
            <button
              key={tab}
              className={`tab ${activeTab === tab ? "active" : ""}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}{" "}
              {(tab === "pending" && `(${pendingJobs.length})`) ||
                (tab === "completed" && `(${completedJobs.length})`) ||
                (tab === "failed" && `(${failedJobs.length})`) ||
                ""}
            </button>
          ))}
        </div>

        <div className="tab-content">
          {activeTab === "new" && (
            <div className="new-job-section">
              <h2>Create a New Job</h2>
              <form className="job-form" onSubmit={handleNewJobSubmit}>
                <div className="form-group">
                  <label>Task Description</label>
                  <textarea
                    placeholder="Example: Get the current stock price for Tesla"
                    value={newJobForm.task}
                    onChange={(e) =>
                      setNewJobForm({ ...newJobForm, task: e.target.value })
                    }
                    rows={5}
                    required
                  />
                  <span className="form-hint">
                    Use natural language - the TundraAgent will route to the right specialist
                  </span>
                </div>

                <div className="form-group">
                  <label>Goal (Optional)</label>
                  <input
                    type="text"
                    placeholder="Additional context or specific requirements"
                    value={newJobForm.goal}
                    onChange={(e) =>
                      setNewJobForm({ ...newJobForm, goal: e.target.value })
                    }
                  />
                  <span className="form-hint">
                    Provide more details about what you want to achieve
                  </span>
                </div>

                <button type="submit" className="btn btn-primary" disabled={submitting}>
                  {submitting ? "Submitting..." : "Submit Job"}
                </button>
              </form>
            </div>
          )}

          {activeTab === "pending" && (
            <div className="pending-section">
              <h2>Pending Jobs</h2>
              {loading ? (
                <p className="empty-state">Loading jobs...</p>
              ) : pendingJobs.length === 0 ? (
                <p className="empty-state">No pending jobs</p>
              ) : (
                <div className="jobs-list">
                  {pendingJobs.map((job) => (
                    <div key={job.job_id} className="job-card">
                      <div className="job-card-header">
                        <span className="job-id">{job.job_id}</span>
                        <span className={`status-badge status-${job.status}`}>
                          {job.status}
                        </span>
                      </div>
                      <h3>{job.task || job.goal}</h3>
                      <div className="job-meta">
                        <span>
                          Agent: <strong>{job.provider_agent || "Waiting for claim"}</strong>
                        </span>
                        <span>
                          Budget: <strong>${job.budget}</strong>
                        </span>
                        <span>
                          Type: <strong>{job.task_type}</strong>
                        </span>
                      </div>
                      {job.status === "in_progress" && (
                        <div className="progress-bar">
                          <div className="progress-fill animating"></div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === "completed" && (
            <div className="completed-section">
              <h2>Completed Jobs</h2>
              {loading ? (
                <p className="empty-state">Loading jobs...</p>
              ) : completedJobs.length === 0 ? (
                <p className="empty-state">No completed jobs yet</p>
              ) : (
                completedJobs.map((job) => (
                  <div key={job.job_id} className="job-card completed">
                    <div className="job-card-header">
                      <span className="job-id">{job.job_id}</span>
                      <span className="status-badge status-completed">
                        Completed
                      </span>
                    </div>
                    <h3>{job.task || job.goal}</h3>
                    <div className="job-meta">
                      <span>
                        Agent: <strong>{job.provider_agent}</strong>
                      </span>
                      <span>
                        Cost: <strong>${job.budget}</strong>
                      </span>
                      <span>
                        Time: <strong>
                          {job.completed_at && job.created_at
                            ? `${Math.round((new Date(job.completed_at) - new Date(job.created_at)) / 1000)}s`
                            : "N/A"}
                        </strong>
                      </span>
                    </div>
                    <div className="job-output">
                      <strong>Result:</strong>
                      <pre style={{ whiteSpace: "pre-wrap", marginTop: "8px", fontSize: "12px" }}>
                        {JSON.stringify(job.result, null, 2)}
                      </pre>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === "failed" && (
            <div className="disputed-section">
              <h2>Failed Jobs</h2>
              {loading ? (
                <p className="empty-state">Loading jobs...</p>
              ) : failedJobs.length === 0 ? (
                <p className="empty-state">No failed jobs</p>
              ) : (
                failedJobs.map((job) => (
                  <div key={job.job_id} className="job-card disputed">
                    <div className="job-card-header">
                      <span className="job-id">{job.job_id}</span>
                      <span className="status-badge status-error">Failed</span>
                    </div>
                    <h3>{job.task || job.goal}</h3>
                    <div className="job-meta">
                      <span>
                        Agent: <strong>{job.provider_agent || "Not assigned"}</strong>
                      </span>
                      <span>
                        Budget: <strong>${job.budget}</strong>
                      </span>
                    </div>
                    <div className="job-output">
                      <strong>Error:</strong> {job.error || "Unknown error"}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Jobs;
