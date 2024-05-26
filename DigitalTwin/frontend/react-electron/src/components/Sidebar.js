// src/components/Sidebar.js

import React from 'react';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faRandom, faRobot, faCar, faMotorcycle, faBicycle, faPersonWalking, faBroom, faRoadBarrier, faArrowRightFromBracket, faHouse } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link } from 'react-router-dom';
import './Sidebar.css';
import { Tooltip } from 'react-tooltip';


library.add(faRandom, faRobot, faCar, faMotorcycle, faBicycle, faPersonWalking, faBroom, faRoadBarrier, faArrowRightFromBracket, faHouse);
function Sidebar() {
 return (
    <div className="sidebar">
      <div className="sidebar-content">
        <div className="sidebar-cards">
          <Link to="/simulation">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon="house" size="2x" />
              </div>
              <h2>Simulation Page</h2>
            </div>
          </Link>
          <Link to="/addRandom" data-tooltip-id="Firsttooltip"
                data-tooltip-content="Add vehicles with random directions"
                data-tooltip-place="bottom">
          <div className="card">
            <div className="card-icon">
              <FontAwesomeIcon icon="random" size="2x" />
            </div>
            <h2>Random</h2>
          </div>
          </Link>
          <Link to="/car">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon={faCar} size="2x" />
              </div>
              <h2>Car</h2>
            </div>
          </Link>
          <Link to="/block">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon={faRoadBarrier} size="2x" />
              </div>
              <h2>Block</h2>
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
          <Link to="/clear">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon="broom" size="2x" />
              </div>
              <h2>Clear Simulation</h2>
            </div>
          </Link>
          <Link to="/endSimulation">
            <div className="card">
              <div className="card-icon">
                <FontAwesomeIcon icon="arrow-right-from-bracket" size="2x" />
              </div>
              <h2>End the Simulation</h2>
            </div>
          </Link>
        </div>
      </div>
      <Tooltip id="Firsttooltip"/>

    </div>
 );
}

export default Sidebar;
