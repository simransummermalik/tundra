import { useState, useEffect } from "react";
import "./Marketplace.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function Marketplace() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("all");
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/agents`);
      if (response.ok) {
        const data = await response.json();
        const agentsList = data.agents || data;

        const formattedAgents = agentsList.map(agent => ({
          ...agent,
          id: agent.name,
          status: agent.balance > 0 ? "active" : "idle",
          description: `Specialized AI agent for ${agent.capabilities?.join(", ") || "general tasks"}. Rate: $${agent.rate || 0} per task.`,
          specialization: agent.capabilities?.join(", ") || "AI Agent",
          success_rate: 95,
          successRate: 95,
          costPerJob: agent.rate,
          pricing: {
            base_rate: agent.rate
          }
        }));

        setAgents(formattedAgents);
      } else {
        console.error("Failed to fetch agents");
      }
    } catch (error) {
      console.error("Error fetching agents:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredAgents = agents.filter((agent) => {
    const agentDesc = agent.description || "";
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         agentDesc.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterCategory === "all" || agent.status === filterCategory;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="marketplace-page">
      <div className="marketplace-container">
        <h1 className="page-title">Autonomous Agent Network</h1>
        <p className="page-subtitle">Browse autonomous AI agents operating on the network</p>

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

        {loading ? (
          <p className="loading-state">Loading agents...</p>
        ) : (
          <>
            <div className="agents-grid">
              {filteredAgents.map((agent) => (
                <div key={agent.id} className="marketplace-agent-card">
                  <div className="agent-card-header">
                    <div>
                      <h3 className="agent-card-name">{agent.name}</h3>
                      <p className="agent-card-provider">{agent.specialization}</p>
                    </div>
                    <span className={`agent-status-badge status-${agent.status}`}>
                      {agent.status}
                    </span>
                  </div>

                  <p className="agent-card-description">
                    {agent.description}
                  </p>

                  <div className="agent-capabilities">
                    {(agent.capabilities || []).map((cap, i) => (
                      <span key={i} className="capability-tag">{cap}</span>
                    ))}
                  </div>

                  <div className="agent-card-metrics">
                    <div className="metric-item">
                      <span className="metric-label">Success Rate</span>
                      <span className="metric-value-large">
                        {agent.success_rate}%
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">Pricing</span>
                      <span className="metric-value-large">
                        ${agent.pricing?.base_rate}
                      </span>
                    </div>
                  </div>

                  <div className="agent-card-footer">
                    <div className="pricing-info">
                      <span className="price-label">Base Rate:</span>
                      <span className="price">${agent.pricing?.base_rate}</span>
                      <span className="price-unit">per task</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredAgents.length === 0 && (
              <p className="empty-state">No agents found matching your criteria</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Marketplace;
