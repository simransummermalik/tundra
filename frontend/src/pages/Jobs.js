import { useState } from "react";
import "./Jobs.css";

function Jobs() {
  const [activeTab, setActiveTab] = useState("new");
  const [newJobForm, setNewJobForm] = useState({
    task: "",
    budget: "",
    preferredAgent: "auto",
  });

  // Placeholder jobs data
  const pendingJobs = [
    {
      id: "JOB-9819",
      task: "Validate CSV data compliance",
      agent: "ValidatorPro",
      budget: 0.12,
      status: "processing",
      progress: 45,
    },
    {
      id: "JOB-9818",
      task: "Analyze code repository for vulnerabilities",
      agent: "CodeReview-AI",
      budget: 0.22,
      status: "queued",
      progress: 0,
    },
  ];

  const completedJobs = [
    {
      id: "JOB-9821",
      task: "Scrape product data from e-commerce site",
      agent: "DataScraper-AI",
      cost: 0.15,
      time: "2.1s",
      rating: null,
      output: "Successfully scraped 1,245 products",
    },
    {
      id: "JOB-9820",
      task: "Summarize research paper (15 pages)",
      agent: "SummarizeGPT",
      cost: 0.08,
      time: "1.9s",
      rating: 5,
      output: "Generated 500-word summary",
    },
  ];

  const disputedJobs = [
    {
      id: "JOB-9750",
      task: "Extract structured data from PDFs",
      agent: "DataExtractor-Pro",
      cost: 0.18,
      reason: "Incomplete output - missing 30% of data",
      status: "Under Review",
    },
  ];

  const handleNewJobSubmit = (e) => {
    e.preventDefault();
    console.log("New job:", newJobForm);
    // TODO: Submit to API
    alert("Job submitted! (This will connect to backend later)");
    setNewJobForm({ task: "", budget: "", preferredAgent: "auto" });
  };

  return (
    <div className="jobs-page">
      <div className="jobs-container">
        <h1 className="page-title">Job Management</h1>
        <p className="page-subtitle">Create, track, and manage your AI agent jobs</p>

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === "new" ? "active" : ""}`}
            onClick={() => setActiveTab("new")}
          >
            New Job
          </button>
          <button
            className={`tab ${activeTab === "pending" ? "active" : ""}`}
            onClick={() => setActiveTab("pending")}
          >
            Pending ({pendingJobs.length})
          </button>
          <button
            className={`tab ${activeTab === "completed" ? "active" : ""}`}
            onClick={() => setActiveTab("completed")}
          >
            Completed ({completedJobs.length})
          </button>
          <button
            className={`tab ${activeTab === "disputed" ? "active" : ""}`}
            onClick={() => setActiveTab("disputed")}
          >
            Disputed ({disputedJobs.length})
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {/* NEW JOB TAB */}
          {activeTab === "new" && (
            <div className="new-job-section">
              <h2>Create a New Job</h2>
              <form className="job-form" onSubmit={handleNewJobSubmit}>
                <div className="form-group">
                  <label>Task Description</label>
                  <textarea
                    placeholder="Describe what you need done (e.g., 'Scrape all product listings from https://example.com')"
                    value={newJobForm.task}
                    onChange={(e) => setNewJobForm({ ...newJobForm, task: e.target.value })}
                    rows={5}
                    required
                  />
                  <span className="form-hint">Use natural language - our routing AI will understand</span>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Budget ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0.03"
                      placeholder="0.15"
                      value={newJobForm.budget}
                      onChange={(e) => setNewJobForm({ ...newJobForm, budget: e.target.value })}
                      required
                    />
                    <span className="form-hint">Minimum $0.03</span>
                  </div>

                  <div className="form-group">
                    <label>Preferred Agent</label>
                    <select
                      value={newJobForm.preferredAgent}
                      onChange={(e) => setNewJobForm({ ...newJobForm, preferredAgent: e.target.value })}
                    >
                      <option value="auto">Auto-select (Recommended)</option>
                      <option value="DataScraper-AI">DataScraper-AI</option>
                      <option value="SummarizeGPT">SummarizeGPT</option>
                      <option value="ValidatorPro">ValidatorPro</option>
                      <option value="CodeReview-AI">CodeReview-AI</option>
                    </select>
                  </div>
                </div>

                <button type="submit" className="btn btn-primary">
                  Submit Job
                </button>
              </form>
            </div>
          )}

          {/* PENDING TAB */}
          {activeTab === "pending" && (
            <div className="pending-section">
              <h2>Pending Jobs</h2>
              {pendingJobs.length === 0 ? (
                <p className="empty-state">No pending jobs</p>
              ) : (
                <div className="jobs-list">
                  {pendingJobs.map((job) => (
                    <div key={job.id} className="job-card">
                      <div className="job-card-header">
                        <span className="job-id">{job.id}</span>
                        <span className={`status-badge status-${job.status}`}>
                          {job.status}
                        </span>
                      </div>
                      <h3>{job.task}</h3>
                      <div className="job-meta">
                        <span>Agent: <strong>{job.agent}</strong></span>
                        <span>Budget: <strong>${job.budget}</strong></span>
                      </div>
                      {job.progress > 0 && (
                        <div className="progress-bar">
                          <div className="progress-fill" style={{ width: `${job.progress}%` }}></div>
                          <span className="progress-text">{job.progress}%</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* COMPLETED TAB */}
          {activeTab === "completed" && (
            <div className="completed-section">
              <h2>Completed Jobs</h2>
              {completedJobs.map((job) => (
                <div key={job.id} className="job-card completed">
                  <div className="job-card-header">
                    <span className="job-id">{job.id}</span>
                    <span className="status-badge status-completed">Completed</span>
                  </div>
                  <h3>{job.task}</h3>
                  <div className="job-meta">
                    <span>Agent: <strong>{job.agent}</strong></span>
                    <span>Cost: <strong>${job.cost}</strong></span>
                    <span>Time: <strong>{job.time}</strong></span>
                  </div>
                  <div className="job-output">
                    <strong>Output:</strong> {job.output}
                  </div>
                  <div className="job-actions">
                    {!job.rating && (
                      <button className="btn-small">Rate Job</button>
                    )}
                    <button className="btn-small">View Receipt</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* DISPUTED TAB */}
          {activeTab === "disputed" && (
            <div className="disputed-section">
              <h2>Disputed Jobs</h2>
              {disputedJobs.length === 0 ? (
                <p className="empty-state">No disputed jobs</p>
              ) : (
                disputedJobs.map((job) => (
                  <div key={job.id} className="job-card disputed">
                    <div className="job-card-header">
                      <span className="job-id">{job.id}</span>
                      <span className="status-badge status-error">{job.status}</span>
                    </div>
                    <h3>{job.task}</h3>
                    <div className="job-meta">
                      <span>Agent: <strong>{job.agent}</strong></span>
                      <span>Cost: <strong>${job.cost}</strong></span>
                    </div>
                    <div className="dispute-reason">
                      <strong>Reason:</strong> {job.reason}
                    </div>
                    <div className="job-actions">
                      <button className="btn-small btn-primary">Request Refund</button>
                      <button className="btn-small">View Details</button>
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
