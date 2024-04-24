import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCar, faTrash, faEdit } from '@fortawesome/free-solid-svg-icons';
import './VehicleCard.css';

const Card = ({ id, onDelete, handleEdit }) => {
 return (
    <div className="card-vehicle">
      <div className="card-icon-vehicle">
        <FontAwesomeIcon icon={faCar} size="2x" />
      </div>
      <h2>{id}</h2>
      <div className="card-buttons-vehicle">
          <button onClick={handleEdit}>
            <FontAwesomeIcon icon={faEdit} size="lg" />
          </button>
          <button onClick={onDelete}>
            <FontAwesomeIcon icon={faTrash} size="lg" />
          </button>
      </div>
    </div>
 );
};

export default Card;
