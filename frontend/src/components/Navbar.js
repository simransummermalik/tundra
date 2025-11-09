import { Link } from "react-router-dom";
import { supabase } from "../supabaseClient";
import "./Navbar.css";
import logo from "../assets/logo.png";

function Navbar({ session }) {
  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img src={logo} alt="Tundra Logo" className="navbar-logo" />
        <span className="navbar-title">TUNDRA</span>
      </div>

      <ul className="navbar-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/agents">Agents</Link></li>
        <li><Link to="/jobs">Jobs</Link></li>
        <li><Link to="/transactions">Transactions</Link></li>
        <li><Link to="/settings">Settings</Link></li>
      </ul>

      <div className="navbar-right">
        <span className="user-email">{session?.user?.email}</span>
        <button onClick={handleLogout} className="btn-logout">Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;

