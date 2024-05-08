// src/components/Navbar.js

import React, { useContext, useEffect } from 'react';
import './Navbar.css';

function Navbar() {

  const getUserName = () => {
    localStorage.getItem('username');
    console.log(localStorage.getItem('username'));
    return localStorage.getItem('username') || 'Login';
  };

  useEffect(() => {
    getUserName();
  }
  , []);

 return (
    <nav className="navbar">
      <div className="navbar-content" >
        <div className="navbar-logo">
          <a href="/"><h1>Digital Twin</h1></a>
        </div>
        <div className="navbar-links">
          <a href="/login">{getUserName()}</a>
          <a href="/settings">Settings</a>
        </div>
      </div>
    </nav>
 );
}

export default Navbar;
