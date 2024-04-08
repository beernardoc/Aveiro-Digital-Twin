import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './CarPage.css';

const CarPage = () => {
 const [quantity, setQuantity] = useState('');
 const [initialCoordinates, setInitialCoordinates] = useState('');
 const [finalCoordinates, setFinalCoordinates] = useState('');
 const [speed, setSpeed] = useState('');
 const [orientationAngle, setOrientationAngle] = useState('');

 const handleCancel = () => {
    window.location.href = '/';
 };

 const handleAdd = () => {
    window.location.href = '/';
 };

 return (
    <div className="car-page-container">
        <div className="car-page">
        <h1>Car Details</h1>
        <form>
            <label>
            Quantity:
            <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
            </label>
            <label>
            Initial Coordinates:
            <input type="text" value={initialCoordinates} onChange={(e) => setInitialCoordinates(e.target.value)} />
            </label>
            <label>
            Final Coordinates:
            <input type="text" value={finalCoordinates} onChange={(e) => setFinalCoordinates(e.target.value)} />
            </label>
            <label>
            Speed:
            <input type="number" value={speed} onChange={(e) => setSpeed(e.target.value)} />
            </label>
            <label>
            Orientation Angle:
            <input type="number" value={orientationAngle} onChange={(e) => setOrientationAngle(e.target.value)} />
            </label>
        </form>
        <div className="buttons-container">
            <button className="cancel-button" onClick={handleCancel}>Cancel</button>
            <button className="add-button" onClick={handleAdd}>Add</button>
        </div>
        </div>
    </div>
 );
};

export default CarPage;
