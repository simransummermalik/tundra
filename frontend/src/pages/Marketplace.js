import { useState } from "react";
import "./Marketplace.css";

function Marketplace() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("all");

  const agents = [
    {
      id: 1,
      name: "DataScraper-AI",
      provider: "ScrapeTech Labs",
      description: "High-performance web scraper with JavaScript rendering support. Handles dynamic content, pagination, and complex site structures.",
      capabilities: ["Web Scraping", "Data Extraction", "API Integration"],
      pricing: 0.15,
      region: "US-East",
      status: "active",
      metrics: {
        successRate: 94,
        avgLatency: "2.3s",
        jobsCompleted: 1247,
        rating: 4.8,
      },
      verified: true,
    },
    {
      id: 2,
      name: "SummarizeGPT",
      provider: "TextAI Solutions",
      description: "Advanced summarization agent powered by GPT-4. Supports multiple languages and customizable summary lengths.",
      capabilities: ["Text Summarization", "Translation", "Sentiment Analysis"],
      pricing: 0.08,
      region: "EU-West",
      status: "active",
      metrics: {
        successRate: 91,
        avgLatency: "1.8s",
        jobsCompleted: 3421,
        rating: 4.9,
      },
      verified: true,
    },
    {
      id: 3,
      name: "ValidatorPro",
      provider: "DataGuard Inc",
      description: "Comprehensive data validation agent. Checks compliance, format correctness, and data integrity across multiple standards.",
      capabilities: ["Data Validation", "Compliance Checking", "Schema Verification"],
      pricing: 0.12,
      region: "US-West",
      status: "active",
      metrics: {
        successRate: 89,
        avgLatency: "3.1s",
        jobsCompleted: 892,
        rating: 4.6,
      },
      verified: true,
    },
    {
      id: 4,
      name: "CodeReview-AI",
      provider: "DevSecure",
      description: "Automated code review and security analysis. Detects vulnerabilities, code smells, and suggests improvements.",
      capabilities: ["Code Review", "Security Analysis", "Best Practices"],
      pricing: 0.22,
      region: "US-East",
      status: "active",
      metrics: {
        successRate: 85,
        avgLatency: "4.5s",
        jobsCompleted: 567,
        rating: 4.7,
      },
      verified: false,
    },
    {
      id: 5,
      name: "ImageAnalyzer-Pro",
      provider: "VisionTech",
      description: "Computer vision agent for image classification, object detection, and content moderation.",
      capabilities: ["Image Classification", "Object Detection", "OCR"],
      pricing: 0.18,
      region: "Asia-Pacific",
      status: "idle",
      metrics: {
        successRate: 92,
        avgLatency: "2.9s",
        jobsCompleted: 2103,
        rating: 4.8,
      },
      verified: true,
    },
  ];

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterCategory === "all" || agent.status === filterCategory;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="marketplace-page">
      <div className="marketplace-container">
        <h1 className="page-title">Agent Marketplace</h1>
        <p className="page-subtitle">Discover and hire AI agents for your tasks</p>

        {/* Search and Filter */}
        <div className="marketplace-controls">
          <input
            type="text"
            placeholder="Search agents..."
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select
            className="filter-select"
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
          >
            <option value="all">All Agents</option>
            <option value="active">Active Only</option>
            <option value="idle">Idle Only</option>
          </select>
        </div>

        {/* Agents Grid */}
        <div className="agents-grid">
          {filteredAgents.map((agent) => (
            <div key={agent.id} className="marketplace-agent-card">
              <div className="agent-card-header">
                <div>
                  <h3 className="agent-card-name">
                    {agent.name}
                    {agent.verified && <span className="verified-badge">✓ Verified</span>}
                  </h3>
                  <p className="agent-card-provider">by {agent.provider}</p>
                </div>
                <span className={`agent-status-badge status-${agent.status}`}>
                  {agent.status}
                </span>
              </div>

              <p className="agent-card-description">{agent.description}</p>

              <div className="agent-capabilities">
                {agent.capabilities.map((cap, i) => (
                  <span key={i} className="capability-tag">{cap}</span>
                ))}
              </div>

              <div className="agent-card-metrics">
                <div className="metric-item">
                  <span className="metric-label">Success Rate</span>
                  <span className="metric-value-large">{agent.metrics.successRate}%</span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Latency</span>
                  <span className="metric-value-large">{agent.metrics.avgLatency}</span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Jobs</span>
                  <span className="metric-value-large">{agent.metrics.jobsCompleted.toLocaleString()}</span>
                </div>
                <div className="metric-item">
                  <span className="metric-value-large">★ {agent.metrics.rating}</span>
                  <span className="metric-label">Rating</span>
                </div>
              </div>

              <div className="agent-card-footer">
                <div className="pricing">
                  <span className="price">${agent.pricing}</span>
                  <span className="price-unit">per job</span>
                </div>
                <button className="btn btn-primary">Hire Agent</button>
              </div>
            </div>
          ))}
        </div>

        {filteredAgents.length === 0 && (
          <p className="empty-state">No agents found matching your criteria</p>
        )}
      </div>
    </div>
  );
}

export default Marketplace;
