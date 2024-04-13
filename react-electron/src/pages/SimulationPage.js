import React, { useState } from 'react';
import Card from '../components/VehicleCard';
import { faRandom, faCar, faMotorcycle } from '@fortawesome/free-solid-svg-icons';
import './SimulationPage.css';
import Navbar from "../components/Navbar";

const SimulationPage = () => {
 const [cards, setCards] = useState([
    { id: 1, title: 'Car 1', icon: faCar },
    { id: 2, title: 'Car 2', icon: faCar },
    { id: 3, title: 'Car 3', icon: faCar },
    { id: 4, title: 'Car 4', icon: faCar },
    { id: 5, title: 'Car 5', icon: faCar },
    { id: 6, title: 'Motorcycle 1', icon: faMotorcycle },
    { id: 7, title: 'Motorcycle 2', icon: faMotorcycle },
    { id: 8, title: 'Motorcycle 3', icon: faMotorcycle },
 ]);

 const handleDelete = (id) => {
    setCards(cards.filter(card => card.id !== id));
 };

 return (
     <div>


    <div className="simulation-page-container">
        <div className="main-content">
        <div className="sidebar-cards">
            {cards.map(card => (
            <Card key={card.id} title={card.title} icon={card.icon} onDelete={() => handleDelete(card.id)} />
            ))}
        </div>
            <button className="simulate-button" onClick={() => console.log('Simular')}>Simular</button>
        </div>
    </div>
    </div>
 );
};

export default SimulationPage;
