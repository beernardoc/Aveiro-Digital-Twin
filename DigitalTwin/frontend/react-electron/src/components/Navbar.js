import React, { useState, useEffect, useRef } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState(localStorage.getItem('username') || 'Login');
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const dropdownRef = useRef(null);

  const getUserName = () => {
    const storedUsername = localStorage.getItem('username');
    console.log(storedUsername);
    return storedUsername || 'Login';
  };

  useEffect(() => {
    setUsername(getUserName());
  }, [location]);

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    setUsername('Login');
    setDropdownVisible(false);
    navigate('/');
  };

  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setDropdownVisible(false);
    }
  };

  useEffect(() => {
    if (dropdownVisible) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownVisible]);

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-logo">
          <Link to="/"><h1>Digital Twin</h1></Link>
        </div>
        <div className="navbar-links">
          {username === 'Login' ? (
            <Link to="/login">{username}</Link>
          ) : (
            <div className="dropdown" ref={dropdownRef}>
              <button onClick={toggleDropdown} className="dropdown-toggle">
                {username}
              </button>
              {dropdownVisible && (
                <div className="dropdown-menu">
                  <Link to="/history">View History</Link>
                  <button onClick={handleLogout} style={{ color: '#EE4E4E' }}>Log Out</button>
                </div>
              )}
            </div>
          )}
          <Link to="/settings">Settings</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
