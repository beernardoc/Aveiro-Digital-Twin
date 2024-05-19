import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClockRotateLeft, faRoad } from '@fortawesome/free-solid-svg-icons';
import './HistoryCard.css';
import axios from 'axios';

const Card = ({ date, simulation_name, _id }) => {
    // date is like: "2024-05-18T23:24:56.070Z", so we need to format it
    const dateObj = new Date(date);
    const formattedDate = dateObj.toLocaleString();

    const handleClick = () => {
        // Redirect to the simulation page with the simulation id
        axios.get(`http://localhost:5000/api/sim_running`)
            .then((response) => {
                if (response.data.sim_running === false) {
                    axios.post(`http://localhost:5000/api/resimulation?id=${_id}`)
                        .then((response) => {
                            console.log('Comando executado com sucesso:', response.data);
                            window.location.href = '/simulation';
                        })
                        .catch((error) => {
                            console.error('Erro ao executar o comando:', error);
                        });
                } else {
                    alert('There is a simulation running. Please wait until it finishes.');
                }
            })
            .catch((error) => {
                console.error('Erro ao executar o comando:', error);
            });
    };

    return (
        <div className="card-history">
            <div className="card-icon-history">
                <FontAwesomeIcon icon={faClockRotateLeft} size="2x" />
            </div>
            <h2><b>{ simulation_name }</b></h2>
            <p style={{ paddingLeft: '10px' }}><b>|</b></p>
            <p style={{ paddingLeft: '10px' }}>{formattedDate}</p>
            <div className="card-buttons-history">
                <button onClick={handleClick}>
                    <FontAwesomeIcon icon={faRoad} size="lg" /> Resimulate
                </button>
            </div>
        </div>
    );
};

export default Card;
