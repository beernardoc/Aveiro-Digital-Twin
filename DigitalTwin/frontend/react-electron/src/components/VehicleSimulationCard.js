import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCar, faTrash, faEdit } from '@fortawesome/free-solid-svg-icons';
import './VehicleSimulationCard.css';

const VehicleCard = ({ id }) => {
 return (
    <div className="card-simulation-vehicle">
      <div className="card-simulation-icon-vehicle">
        <FontAwesomeIcon icon={faCar} size="2x" />
      </div>

      <div className="card-simulation-text">
        <h2><b>{id}</b></h2>
        <h2>Velocity</h2>
        <h2>Coordinates</h2>
      </div>
    </div>
 );
};

export default VehicleCard;
