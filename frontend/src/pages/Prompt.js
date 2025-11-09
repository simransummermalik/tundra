import React, { useState } from "react";
import "./Prompt.css";

function Prompt() {
  //task and budget
  const [task, setTask] = useState("");
  const [budget, setBudget] = useState("");

  //handling submissions
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Task:", task);
    console.log("Budget:", budget);
    alert("Job submitted! (Mock)");
  };

  //prompt page
  return (
    <div className="prompt-page">
      <h1>Create a Job</h1>
      <form onSubmit={handleSubmit} className="prompt-form">
        <label>
          Task Description:
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Describe what you want the AI to do..."
            required
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
          />
        </label>
        <button type="submit">Submit Job</button>
      </form>
    </div>
  );
}

export default Prompt;
