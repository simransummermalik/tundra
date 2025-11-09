import React from "react";
import "./Profile.css";

function Profile() {
  return (
    //profile information
    <div className="profile-page">
      <h1>Your Profile</h1>
      <div className="profile-section">
        <h2>Account Info</h2>
        <p>Email: user@tundra.ai</p>
        <p>Joined: November 2025</p>
      </div>
      {/* list active jobs */}
      <div className="profile-section">
        <h2>Active Jobs</h2>
      </div>
      {/* list transaction summary with total jobs and total spent */}
      <div className="profile-section">
        <h2>Transaction Summary</h2>
      </div>
    </div>
  );
}

export default Profile;
