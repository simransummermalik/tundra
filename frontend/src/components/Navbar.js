import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar(){
    return(
        <nav classname="navbar">   
            <h2 className="logo">TUNDRA</h2>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/marketplace">Marketplace</Link></li>
                <li><Link to="/profile">Profile</Link></li>
                <li><Link to="/prompt">Create Job</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;