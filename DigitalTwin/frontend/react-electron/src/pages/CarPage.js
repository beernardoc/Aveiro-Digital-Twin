import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './CarPage.css';
import {MapContainer} from "react-leaflet";
import MapComponent from "../components/MapComponent";

const CarPage = () => {
 const [quantity, setQuantity] = useState('');
 const [initialCoordinates, setInitialCoordinates] = useState('');
 const [finalCoordinates, setFinalCoordinates] = useState('');
 const [speed, setSpeed] = useState('');
 const [orientationAngle, setOrientationAngle] = useState('');

 return (
    <div className="car-page-container">
        <div className="car-page">
            <div className="instructions">
                <h2>How to Add a Car:</h2>
                <div className="step">
                    <span className="step-number">Step 1:</span>
                    <span>Click the "Start Position" button and choose on the map where you want your car to start.</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 2:</span>
                    <span>Click the "Finish Position" button and choose where on the map your car's destination is.</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 3:</span>
                    <span>Click "Add a car".</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 4:</span>
                    <span>Choose how many cars and their departure time.</span>
                </div>
            </div>

            <MapComponent/>

        </div>
    </div>
 );
};

export default CarPage;
