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
                <p>
                    You can view the simulation running in different environments: 
                    <strong> Sumo</strong> for 2D simulations and <strong>Carla</strong> for 3D simulations.
                </p>
                <div className="simulation-info-card">
                    <h1><b> Simulation Info</b></h1>
                    <br />
                    <p className='quantity-card'><h4><FontAwesomeIcon icon={faClock} /> Time (s)</h4> {parsedMessage.time}</p>
                    <p className='quantity-card'><h4><FontAwesomeIcon icon={faCar} /> Total Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.quantity}</p>
                    <p className='quantity-card'><h4>Simulated Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.filter(id => id.startsWith('simulated')).length}</p>
                    <p className='quantity-card'><h4>Real Data Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.filter(id => id.startsWith('realdata')).length}</p>
                    <p className='quantity-card'><h4>Live Data Vehicles</h4> {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.filter(id => id.startsWith('livedata')).length}</p>
                    <h4>Legend</h4>
                    <ul>
                        <li><span className="legend-color" style={{ backgroundColor: 'red' }}></span> Real data</li>
                        <li><span className="legend-color" style={{ backgroundColor: 'green' }}></span> Live data</li>
                        <li><span className="legend-color" style={{ backgroundColor: 'yellow' }}></span> Simulated</li>
                    </ul>
                </div>
                <div className="simulation-methods-info">
                    <h3>Simulation Methods</h3>
                    <p>
                        The simulation can use various methods to generate vehicle data:
                    </p>
                    <ul>
                        <li><b>Real Data:</b> This data comes from actual vehicles on the road, collected through sensors and other monitoring equipment.</li>
                        <li><b>Live Data:</b> This data is captured in real-time from live traffic feeds and other dynamic sources.</li>
                        <li><b>Simulated Data:</b> This data is generated through computational models that simulate traffic conditions based on predefined parameters and scenarios.</li>
                    </ul>
                </div>
            </>
        )}
    </div>
</div>


    );
};

export default SimulationPage;
