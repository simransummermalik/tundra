import React from "react";
import "./Marketplace.css";

function Marketplace() {
  const agents = [
    {/* list agents with information on specialization, cost, name, rating, etc. */}
  ];

  return (
    <div className="marketplace-page">
      <h1>Marketplace</h1>
      <p>Browse and hire specialized AI agents.</p>
      <div className="agents-grid">
        {agents.map((agent, index) => (
          <div key={index} className="agent-card">
            <h2>{agent.name}</h2>
            <p>Specialty: {agent.spec}</p>
            <p>Price: ${agent.price}</p>
            <p>Reputation: {agent.reputation}</p>
            <button>Hire</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Marketplace;
