import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClockRotateLeft, faRoad, faTrash } from '@fortawesome/free-solid-svg-icons';
import './HistoryCard.css';
import axios from 'axios';

const Card = ({ date, simulation_name, _id, handleClick, handleDelete }) => {
    // date is like: "2024-05-18T23:24:56.070Z", so we need to format it
    const dateObj = new Date(date);
    const formattedDate = dateObj.toLocaleString();

    return (
        <div className="card-history">
            <div className="card-icon-history">
                <FontAwesomeIcon icon={faClockRotateLeft} size="2x" />
            </div>
            <h2><b>{ simulation_name }</b></h2>
            <p style={{ paddingLeft: '10px' }}><b>|</b></p>
            <p style={{ paddingLeft: '10px' }}>{formattedDate}</p>
            <div className="card-buttons-history">
                <button onClick={handleClick} style={{ marginRight: '90px' }}>
                    <FontAwesomeIcon icon={faRoad} size="lg" /> Resimulate
                </button>
            </div>
            <button onClick={handleDelete}>
                <FontAwesomeIcon icon={faTrash} size="lg" /> Delete
            </button>
        </div>
    );
};

export default Card;