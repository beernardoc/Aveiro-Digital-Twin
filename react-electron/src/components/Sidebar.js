// src/components/Sidebar.js

import React from 'react';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faRandom, faRobot, faCar, faMotorcycle, faBicycle, faPersonWalking } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link } from 'react-router-dom';
import './Sidebar.css';


library.add(faRandom, faRobot, faCar, faMotorcycle, faBicycle, faPersonWalking);
function Sidebar() {
 return (
    <div className="sidebar">
      <div className="sidebar-content">
        <div className="sidebar-checkbox">
          <input type="checkbox" id="realData" name="realData" />
          <label htmlFor="realData">Real Data</label>
        </div>
        <div className="sidebar-cards">
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="random" size="2x" />
            </div>
            <h2>Random</h2>
          </div>
          <Link to="/car">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon={faCar} size="2x" />
              </div>
              <h2>Car</h2>
            </div>
          </Link>
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="motorcycle" size="2x" />
            </div>
            <h2>Motorcycle</h2>
          </div>
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="bicycle" size="2x" />
            </div>
            <h2>Bicycle</h2>
          </div>
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="person-walking" size="2x" />
            </div>
            <h2>Pedestrian</h2>
          </div>
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="robot" size="2x" />
            </div>
            <h2>Autonomous Vehicle</h2>
          </div>
        </div>
      </div>
    </div>
 );
}

export default Sidebar;
