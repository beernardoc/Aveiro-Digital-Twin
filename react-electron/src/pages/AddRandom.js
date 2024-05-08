import React, { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import './AddRandom.css';
import AddRandomCar_form from "../components/AddRandomCar_form";
import AddRandomPerson_form from "../components/AddRandomPerson_form";
import AddRandomMotorcycle_form from "../components/AddRandomMotorcycle_form";
import AddRandomBike_form from "../components/AddRandomBike_form";


const AddRandom = () => {

    const [quantity, setQuantity] = useState('');
    const [initialCoordinates, setInitialCoordinates] = useState('');
    const [finalCoordinates, setFinalCoordinates] = useState('');
    const [speed, setSpeed] = useState('');
    const [orientationAngle, setOrientationAngle] = useState('');
    const [activeComponent, setActiveComponent] = useState('vehicle');

    const handleCancel = () => {
        window.location.href = '/';
    };

    const handleAdd = () => {
        window.location.href = '/';
    };

    const handleComponentChange = (component) => {
        setActiveComponent(component);
    };

    return (
        <div className="random-page-container">
            <div className="random-page">

                <div className="button-container">
                    <button
                        className={activeComponent === 'vehicle' ? 'active' : ''}
                        onClick={() => handleComponentChange('vehicle')}
                    >
                        Car
                    </button>
                    <button
                        className={activeComponent === 'motorcycle' ? 'active' : ''}
                        onClick={() => handleComponentChange('motorcycle')}
                    >
                        Motorcycle
                    </button>
                    <button
                        className={activeComponent === 'bicycle' ? 'active' : ''}
                        onClick={() => handleComponentChange('bicycle')}
                    >
                        Bicycle
                    </button>

                    <button
                        className={activeComponent === 'person' ? 'active' : ''}
                        onClick={() => handleComponentChange('person')}
                    >
                        Person
                    </button>

                </div>

                {activeComponent === 'vehicle' && <AddRandomCar_form/>}
                {activeComponent === 'person' && <AddRandomPerson_form/>}
                {activeComponent === 'motorcycle' && <AddRandomMotorcycle_form/>}
                {activeComponent === 'bicycle' && <AddRandomBike_form/>}


                {/* Adicione mais componentes conforme necessário */}

            </div>
        </div>
    );
};

export default AddRandom;
