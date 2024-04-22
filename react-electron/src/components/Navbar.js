// src/components/Navbar.js

import React from 'react';
import './Navbar.css';

function Navbar() {
 return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-logo">
          <a href="/"><h1>Digital Twin</h1></a>
        </div>
        <div className="navbar-links">
          <a href="#">User</a>
          <a href="#">Settings</a>
        </div>
      </div>
    </nav>
 );
}

export default Navbar;
