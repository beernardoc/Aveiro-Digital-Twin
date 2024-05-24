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
    return (
        <div className="simulation-page-container">
            <div className="simulation-page">
                {parsedMessage && (
                    <>
                        <div className="time-quantity-card">
                            <div className={`time-card ${faClock}`}>
                                <b><FontAwesomeIcon icon={faClock} /> Time</b>{parsedMessage.time} seconds
                            </div>
                            <div className={`quantity-card ${faCar}`}> 
                                <b> <FontAwesomeIcon icon={faCar} /> Quantity</b> {parsedMessage.vehicle && parsedMessage.vehicle.quantity}
                            </div>
                        </div>
                        <div className="vehicle-cards">
                            {parsedMessage.vehicle && parsedMessage.vehicle.ids && parsedMessage.vehicle.ids.map((id, index) => (
                                <VehicleCard key={index} id={id} />
                            ))}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SimulationPage;
