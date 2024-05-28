import React, { useState, useEffect } from 'react';
import Card from '../components/VehicleCard';
import VehicleCard from '../components/VehicleSimulationCard';
import { faRandom, faCar, faMotorcycle, faClock } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'; // Importe o componente FontAwesomeIcon
import './SimulationPage.css';
import Navbar from "../components/Navbar";
import AddRandom_form from "../components/AddRandomCar_form";
import socketIOClient from 'socket.io-client';

const SimulationPage = () => {
    const [message, setMessage] = useState('');
    const [parsedMessage, setParsedMessage] = useState(null); // Adiciona um novo estado para armazenar o objeto parseado

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000'); 

        socket.on('cars', (data) => {
            // Convertendo a mensagem ArrayBuffer para string
            const decoder = new TextDecoder();
            const decodedMessage = decoder.decode(data);
            
            setMessage(decodedMessage);
            console.log('Mensagem recebida do servidor:', decodedMessage);

            // Convertendo a string JSON em um objeto JavaScript
            const parsed = JSON.parse(decodedMessage);
            setParsedMessage(parsed);
        });

        return () => socket.disconnect();
    }, []);

    // Verifica se a mensagem parseada está disponível antes de tentar acessar suas propriedades
    // random, simulated, realdata
    return (
<div className="simulation-page-container">
    <div className="simulation-page">
        {parsedMessage && (
            <>
                <div className="instructions">
                    <h2>You can view the simulation running in different environments: 
                    <strong> Sumo</strong> for 2D simulations and <strong>Carla</strong> for 3D simulations.
                    </h2>
                </div>
                <div className="simulation-info-card">
                    <h1><b> Simulation Info</b></h1>
                    <br />
                    <p className='quantity-card'><h4><FontAwesomeIcon icon={faClock} /> Time (s)</h4> {parsedMessage.simulation.time}</p>
                    <p className='quantity-card'><h4><FontAwesomeIcon icon={faCar} /> Total Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.quantity}</p>
                    <p className="vehicles-type-card">
                        <h4>Simulated Vehicles</h4> 
                        {parsedMessage.vehicle && parsedMessage.vehicle.ids && 
                            (parsedMessage.vehicle.ids.filter(id => id.startsWith('simulated')).length + 
                            parsedMessage.vehicle.ids.filter(id => id.startsWith('random')).length)}
                    </p>
                    <p className='vehicles-type-card'><h4>Real Data Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.filter(id => id.startsWith('realdata')).length}</p>
                    <p className='vehicles-type-card'><h4>Live Data Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.filter(id => id.startsWith('livedata')).length}</p>
                    <h4>Legend</h4>
                    <ul>
                        <li><span className="legend-color" style={{ backgroundColor: 'red' }}></span> Real data</li>
                        <li><span className="legend-color" style={{ backgroundColor: 'green' }}></span> Live data</li>
                        <li><span className="legend-color" style={{ backgroundColor: 'yellow' }}></span> Simulated</li>
                        <li><span className="legend-color" style={{ backgroundColor: 'blue' }}></span> Pedestrian</li>

                    </ul>
                </div>
                <div className="simulation-methods-info">
                    <h3>Simulation Methods</h3>
                    <ul>
                        <li><b>Live Data:</b> This data comes from actual vehicles on the road, collected through sensors and other monitoring equipment.</li>
                        <li><b>Real Data:</b> Similar to live data, but this method utilizes historical data collected from previous days or hours.</li>
                        <li><b>Simulated Data:</b> The routes of the simulated cars can be either randomly generated or specifically defined.</li>
                        <li><b>Road Block:</b> You can also experiment with traffic flow by blocking roads to observe the resulting traffic patterns.</li>
                        <li><b>Clear Simulation:</b> Clears all vehicles of the simulation</li>
                    </ul>
                </div>
            </>
        )}
    </div>
</div>


    );
};

export default SimulationPage;
