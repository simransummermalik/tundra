import React, { useState } from "react";
import "./Prompt.css";

function Prompt() {
  const [task, setTask] = useState("");
  const [budget, setBudget] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Task:", task);
    console.log("Budget:", budget);
    alert("Job submitted! (Mock)");
    setTask("");
    setBudget("");
  };

  return (
    <div className="prompt-page">
      <div className="prompt-container">
        <h1>Create a Job</h1>
        <p className="page-subtitle">
          Fill out the details below to submit a new job for your AI agents.
        </p>

        <form onSubmit={handleSubmit} className="prompt-form">
          <label>
            Task Description:
            <textarea
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Describe what you want the AI to do..."
              required
              rows={4}
            />
          </label>

          <label>
            Budget ($):
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              placeholder="Set a budget for the job"
              required
              min="0"
              step="0.01"
            />
          </label>

          <button type="submit">Submit Job</button>
        </form>
      </div>
    </div>
  );
}

export default Prompt;

