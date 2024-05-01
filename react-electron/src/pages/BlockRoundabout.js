import React, { useState, useEffect } from 'react';
import './BlockRoundabout.css';
import map from '../asset/map/roundabouts_map.png';
import axios from 'axios';
import socketIOClient from 'socket.io-client';

export default function BlockRoundabout() {
    const [message, setMessage] = useState('');
    const [blockedRoundabouts, setBlockedRoundabouts] = useState(null); // Adiciona um novo estado para armazenar o objeto parseado

    const [showModal, setShowModal] = useState(false); // State to manage modal visibility
    const [showClearModal, setShowClearModal] = useState(false);
    const [roundabout, setRoundabout] = useState(""); // State to manage selected roundabout [1, 2, 3, 4]

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000'); 

        socket.on('blocked_roundabouts', (data) => {
            // Convert the ArrayBuffer message to a string
            const decoder = new TextDecoder();
            const decodedMessage = decoder.decode(data);
            
            setMessage(decodedMessage);

            // Convert the JSON string to a JavaScript object
            const parsed = JSON.parse(decodedMessage);
            // it is a map, get the keys and convert to an array
            const blocked_roundabouts = Object.keys(parsed.blocked_roundabouts)
            setBlockedRoundabouts(blocked_roundabouts);
        });

        return () => socket.disconnect();
    }, []);

    // Function to handle opening the modal
    const handleShow = (id) => {
        axios.get(`http://localhost:5000/api/vehicles`)
        .then(res => {
            const number_of_vehicles = res.data.quantity;
            if (number_of_vehicles > 0) {
                setShowClearModal(true);
            } else {
                setRoundabout(id);
                setShowModal(true);
            }
        });
    };

    // Function to handle closing the modal
    const handleClose = (id) => {
        setShowModal(false);
        setShowClearModal(false);
    };

    // Function to block a roundabout
    const block_roundabout = () => {
        // Send a POST request to the server to block the selected roundabout

        axios.post(`http://localhost:5000/api/blockRoundabout?id=${roundabout}`)
        .then(res => {
            console.log(res.data);
        });

        handleClose();
    }

    return (
        <>
            <div className="roundabout-page-container">
                <div className="roundabout-page">
                    <h1 style={{ color: "black", fontSize: "40px" }}>Block a Roundabout</h1>
                    <h3 style={{ color: "black", fontSize: "20px", paddingBottom: "30px" }}>Select the roundabout you want to block</h3>
                    <div className="roundabout-page-map">
                        {/* Render the map image with clickable areas */}
                        <img src={map} alt="Roundabouts Map" useMap='#roundabout' />

                        {/* Define map areas with onClick events */}
                        <map name="roundabout">
                            <area shape="circle" coords="393,105,10" alt="Roundabout 1" style={{ cursor: "pointer" }} onClick={() => handleShow('1')} />
                            <area shape="circle" coords="551,275,10" alt="Roundabout 2" style={{ cursor: "pointer" }} onClick={() => handleShow('2')} />
                            <area shape="circle" coords="627,611,10" alt="Roundabout 3" style={{ cursor: "pointer" }} onClick={() => handleShow('3')} />
                            <area shape="circle" coords="915,415,10" alt="Roundabout 4" style={{ cursor: "pointer" }} onClick={() => handleShow('4')} />
                        </map>
                    </div>
                </div>
            </div>

            {/* Modal component */}
            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleClose}>&times;</span>
                        <p> Block Roundabout {roundabout}?</p>
                        <div className="modal-buttons">
                            <button className="modal-button-block" style={{ marginRight: "20px" }} onClick={block_roundabout}>Block</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Clear Modal component */}
            {showClearModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleClose}>&times;</span>
                        <p> In Order to Block a Roundabout, There Should not be any Vehicles in the Simulation. Please Clear the Simulation!</p>
                        <div className="modal-buttons">
                            <button className="modal-button-unblock" style={{ marginRight: "20px", width: "300px" }} onClick={() => {window.location.href = '/clear'}}>Go to the Clear Simulation Tab</button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}