import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRotateLeft, faRoad, faTrash } from '@fortawesome/free-solid-svg-icons';
import './BlockedCard.css';

const Card = ({ id, type }) => {
    switch (type) {
        case 'road':
            return (
                <div className="card-vehicle">
                    <div className="card-icon-vehicle">
                        <FontAwesomeIcon icon={faRoad} size="2x" />
                    </div>
                    <h2>Road {id}</h2>
                    <div className="card-buttons-vehicle">
                        <button>
                            <FontAwesomeIcon icon={faTrash} size="lg" /> Unblock
                        </button>
                    </div>
                </div>
            );
        case 'roundabout':
            return (
                <div className="card-vehicle">
                    <div className="card-icon-vehicle">
                        <FontAwesomeIcon icon={faArrowRotateLeft} size="2x" />
                    </div>
                    <h2>Roundabout {id}</h2>
                    <div className="card-buttons-vehicle">
                        <button>
                            <FontAwesomeIcon icon={faTrash} size="lg" /> Unblock
                        </button>
                    </div>
                </div>
            );
        default:
            return null;
    }
};

export default Card;
