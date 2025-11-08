import { Link } from "react-router-dom";
import { supabase } from "../supabaseClient";
import "./Navbar.css";

function Navbar({ session }) {
  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="logo">
          <span className="logo-text">TUNDRA</span>
          <span className="logo-subtitle">Intelligence Self-Governed</span>
        </Link>

        <ul className="nav-links">
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/agents">Agents</Link></li>
          <li><Link to="/jobs">Jobs</Link></li>
          <li><Link to="/transactions">Transactions</Link></li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>

        <div className="nav-user">
          <span className="user-email">{session?.user?.email}</span>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;