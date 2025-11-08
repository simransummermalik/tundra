import { useState } from "react";
import "./Transactions.css";

function Transactions() {
  const [filter, setFilter] = useState("all");

  const transactions = [
    {
      id: "TXN-2024-9821",
      jobId: "JOB-9821",
      task: "Scrape product data from e-commerce site",
      agent: "DataScraper-AI",
      amount: 0.15,
      platform Fee: 0.01,
      totalCharge: 0.16,
      timestamp: "2024-01-15 14:23:11",
      status: "completed",
      tokens: 1250,
      modelVersion: "DataScraper v2.3",
    },
    {
      id: "TXN-2024-9820",
      jobId: "JOB-9820",
      task: "Summarize research paper (15 pages)",
      agent: "SummarizeGPT",
      amount: 0.08,
      platformFee: 0.006,
      totalCharge: 0.086,
      timestamp: "2024-01-15 12:45:33",
      status: "completed",
      tokens: 890,
      modelVersion: "GPT-4-Turbo",
    },
    {
      id: "TXN-2024-9819",
      jobId: "JOB-9819",
      task: "Validate CSV data compliance",
      agent: "ValidatorPro",
      amount: 0.12,
      platformFee: 0.008,
      totalCharge: 0.128,
      timestamp: "2024-01-15 11:12:09",
      status: "processing",
      tokens: null,
      modelVersion: "Validator v1.5",
    },
    {
      id: "TXN-2024-9750",
      jobId: "JOB-9750",
      task: "Extract structured data from PDFs",
      agent: "DataExtractor-Pro",
      amount: 0.18,
      platformFee: 0.013,
      totalCharge: 0.193,
      timestamp: "2024-01-14 18:30:22",
      status: "refunded",
      tokens: 1450,
      modelVersion: "Extractor v3.1",
    },
  ];

  const filteredTransactions = transactions.filter((t) => {
    if (filter === "all") return true;
    return t.status === filter;
  });

  const totalSpent = transactions
    .filter((t) => t.status === "completed")
    .reduce((sum, t) => sum + t.totalCharge, 0);

  const handleExportCSV = () => {
    alert("CSV export will be implemented with backend integration");
  };

  return (
    <div className="transactions-page">
      <div className="transactions-container">
        <h1 className="page-title">Transactions & Reports</h1>
        <p className="page-subtitle">View transaction history and compliance reports</p>

        {/* Summary Stats */}
        <div className="transaction-stats">
          <div className="stat-box">
            <h3>Total Spent (All Time)</h3>
            <p className="stat-big">${totalSpent.toFixed(2)}</p>
          </div>
          <div className="stat-box">
            <h3>Transactions This Month</h3>
            <p className="stat-big">{transactions.length}</p>
          </div>
          <div className="stat-box">
            <h3>Avg. Transaction Size</h3>
            <p className="stat-big">${(totalSpent / transactions.length).toFixed(2)}</p>
          </div>
        </div>

        {/* Controls */}
        <div className="transaction-controls">
          <div className="filter-buttons">
            <button
              className={`filter-btn ${filter === "all" ? "active" : ""}`}
              onClick={() => setFilter("all")}
            >
              All
            </button>
            <button
              className={`filter-btn ${filter === "completed" ? "active" : ""}`}
              onClick={() => setFilter("completed")}
            >
              Completed
            </button>
            <button
              className={`filter-btn ${filter === "processing" ? "active" : ""}`}
              onClick={() => setFilter("processing")}
            >
              Processing
            </button>
            <button
              className={`filter-btn ${filter === "refunded" ? "active" : ""}`}
              onClick={() => setFilter("refunded")}
            >
              Refunded
            </button>
          </div>
          <button className="export-btn" onClick={handleExportCSV}>
            Export CSV
          </button>
        </div>

        {/* Transactions Table */}
        <div className="transactions-table-wrapper">
          <table className="transactions-table">
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Job ID</th>
                <th>Task</th>
                <th>Agent</th>
                <th>Amount</th>
                <th>Platform Fee (7%)</th>
                <th>Total</th>
                <th>Timestamp</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map((txn) => (
                <tr key={txn.id}>
                  <td className="txn-id">{txn.id}</td>
                  <td className="job-id">{txn.jobId}</td>
                  <td className="task-desc">{txn.task}</td>
                  <td>{txn.agent}</td>
                  <td>${txn.amount.toFixed(2)}</td>
                  <td>${txn.platformFee.toFixed(3)}</td>
                  <td className="total-charge">${txn.totalCharge.toFixed(2)}</td>
                  <td className="timestamp">{txn.timestamp}</td>
                  <td>
                    <span className={`txn-status status-${txn.status}`}>
                      {txn.status}
                    </span>
                  </td>
                  <td>
                    <button className="view-receipt-btn">Receipt</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Receipt Details (placeholder) */}
        <div className="compliance-section">
          <h2>Compliance & Audit</h2>
          <p>All transactions are logged with full audit trails including:</p>
          <ul>
            <li>Job summary and output verification</li>
            <li>Timestamps and model versions</li>
            <li>Token usage and pricing breakdown</li>
            <li>Payment status and escrow details</li>
          </ul>
          <p className="compliance-note">
            Exportable reports available in CSV format for accounting and compliance purposes.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Transactions;