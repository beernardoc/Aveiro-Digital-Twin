import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './CarPage.css';
import {MapContainer} from "react-leaflet";
import MapAddCarComponent from "../components/MapAddCarComponent";
import MapAddBikeComponent from "../components/MapAddBikeComponent";
import MapAddPedestrianComponent from "../components/MapAddPedestrianComponent";

const PedestrianPage = () => {
 const [quantity, setQuantity] = useState('');
 const [initialCoordinates, setInitialCoordinates] = useState('');
 const [finalCoordinates, setFinalCoordinates] = useState('');
 const [speed, setSpeed] = useState('');
 const [orientationAngle, setOrientationAngle] = useState('');

 return (
    <div className="car-page-container">
        <div className="car-page">
            <div className="instructions">
                <h2>How to Add a Pedestrian:</h2>
                <div className="step">
                    <span className="step-number">Step 1:</span>
                    <span>Click the "Start Position" button and choose on the map where you want your pedestrian to start.</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 2:</span>
                    <span>Click the "Finish Position" button and choose where on the map your pedestrian destination is.</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 3:</span>
                    <span>Click "Add a bike".</span>
                </div>
                <div className="step">
                    <span className="step-number">Step 4:</span>
                    <span>Choose how many pedestrians and their departure time.</span>
                </div>
            </div>

            <MapAddPedestrianComponent/>

        </div>
    </div>
 );
};

export default PedestrianPage;